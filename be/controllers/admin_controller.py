# controllers/admin_controller.py
from flask import request, jsonify
from services.user_service import UserService
from services.image_service import ImageService
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.image import Image
from functools import wraps
from datetime import datetime, timedelta

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.objects(id=user_id).first()
        
        if not user or user.role != 'admin':
            return jsonify({'error': 'Yêu cầu quyền admin'}), 403
        
        return fn(*args, **kwargs)
    return wrapper

@jwt_required()
@admin_required
def get_all_users():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    is_active = request.args.get('is_active')  # "true", "false", hoặc None
    role = request.args.get('role')           # "admin", "user", hoặc None
    
    users = UserService.get_all_users(
        page=page,
        per_page=per_page,
        is_active=is_active,
        role=role
    )
    
    return jsonify({
        'users': [
            {
                'id': str(user.id),
                'username': user.username,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None,
                'last_login': user.last_login.isoformat() if hasattr(user, 'last_login') and user.last_login else None
            }
            for user in users.items
        ],
        'total': users.total,
        'pages': users.pages,
        'page': users.page
    }), 200

@jwt_required()
@admin_required
def update_user(user_id):
    data = request.get_json()
    
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'error': 'Không tìm thấy người dùng'}), 404
    
    # Cho phép admin cập nhật vai trò
    if 'role' in data:
        user.role = data['role']
    
    # Cập nhật các trường khác
    for key, value in data.items():
        if key != 'password' and hasattr(user, key):
            setattr(user, key, value)
    
    user.save()
    return jsonify({'message': 'Cập nhật người dùng thành công'}), 200

@jwt_required()
@admin_required
def delete_user(user_id):
    success = UserService.delete_user(user_id)
    if not success:
        return jsonify({'error': 'Không tìm thấy người dùng'}), 404
    
    return jsonify({'message': 'Xóa người dùng thành công'}), 200

@jwt_required()
@admin_required
def toggle_user_status(user_id):
    """Bật/tắt trạng thái hoạt động của người dùng"""
    data = request.get_json()
    
    if 'is_active' not in data:
        return jsonify({'error': 'Trạng thái hoạt động (is_active) là bắt buộc'}), 400
    
    try:
        user = UserService.toggle_user_status(user_id, data['is_active'])
        
        return jsonify({
            'message': f"Người dùng đã được {'kích hoạt' if user.is_active else 'khóa'} thành công",
            'user': {
                'id': str(user.id),
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'role': user.role
            }
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Lỗi hệ thống: {str(e)}'}), 500

@jwt_required()
@admin_required
def change_user_role(user_id):
    data = request.get_json()
    
    if 'role' not in data:
        return jsonify({'error': 'Thiếu tham số role'}), 400
    
    try:
        user = UserService.change_user_role(user_id, data['role'])
        
        return jsonify({
            'message': 'Cập nhật vai trò người dùng thành công',
            'user': {
                'id': str(user.id),
                'username': user.username,
                'role': user.role
            }
        }), 200
    except ValueError as e:
        # Xử lý trường hợp không tìm thấy user hoặc role không hợp lệ
        return jsonify({'error': str(e)}), 404
    
    except Exception as e:
        # Bắt các lỗi khác
        return jsonify({'error': f'Lỗi hệ thống: {str(e)}'}), 500

@jwt_required()
@admin_required
def get_all_images():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    
    images = ImageService.get_all_images(page, per_page)
    
    return jsonify({
        'images': [
            {
                'id': str(img.id),
                'description': img.description,
                'url': f"/api/images/file/{str(img.id)}",  # Sửa để sử dụng ID thay vì file_path
                'created_at': img.created_at.isoformat() if hasattr(img, 'created_at') and img.created_at else None,
                'uploaded_by': str(img.uploaded_by.id) if img.uploaded_by else None
            } for img in images.items
        ],
        'total': images.total,
        'pages': images.pages,
        'page': images.page
    }), 200

@jwt_required()
@admin_required
def admin_delete_image(image_id):
    success = ImageService.admin_delete_image(image_id)
    if not success:
        return jsonify({'error': 'Không tìm thấy hình ảnh'}), 404
    
    return jsonify({'message': 'Xóa hình ảnh thành công'}), 200

@jwt_required()
@admin_required
def get_stats():
    """Lấy thống kê cơ bản cho admin dashboard"""
    total_users = User.objects.count()
    total_images = Image.objects.count()
    
    # Thống kê người dùng mới trong 7 ngày qua
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    new_users = User.objects(created_at__gte=seven_days_ago).count()
    
    # Thống kê ảnh mới trong 7 ngày qua
    new_images = Image.objects(created_at__gte=seven_days_ago).count()
    
    return jsonify({
        'total_users': total_users,
        'total_images': total_images,
        'new_users_7d': new_users,
        'new_images_7d': new_images
    }), 200

@jwt_required()
@admin_required
def get_detailed_stats():
    """Lấy thống kê chi tiết cho admin dashboard"""
    # Tổng số liệu
    total_users = User.objects.count()
    total_images = Image.objects.count()
    
    # Thống kê người dùng theo vai trò
    admin_count = User.objects(role='admin').count()
    user_count = User.objects(role='user').count()
    
    # Thống kê người dùng theo trạng thái
    active_users = User.objects(is_active=True).count()
    inactive_users = User.objects(is_active=False).count()
    
    # Thống kê ảnh theo ngày trong 7 ngày qua
    daily_images = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)
        
        count = Image.objects(
            created_at__gte=start_of_day,
            created_at__lt=end_of_day
        ).count()
        
        daily_images.append({
            'date': start_of_day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    return jsonify({
        'totals': {
            'users': total_users,
            'images': total_images
        },
        'users_by_role': {
            'admin': admin_count,
            'user': user_count
        },
        'users_by_status': {
            'active': active_users,
            'inactive': inactive_users
        },
        'daily_images': daily_images
    }), 200