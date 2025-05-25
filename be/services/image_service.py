# services/image_service.py
from models.image import Image
from models.user import User
import uuid
from werkzeug.utils import secure_filename
import io
from flask import send_file

class ImageService:
    
    @staticmethod
    def upload_image(file, description, user_id, location=None):
        """Tải lên hình ảnh mới vào MongoDB"""
        # Tạo tên tệp duy nhất
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Đọc dữ liệu nhị phân từ file
        file_data = file.read()
        
        # Tạo bản ghi hình ảnh
        user = User.objects(id=user_id).first()
        image = Image(
            description=description,
            file_name=unique_filename,
            content_type=file.content_type,
            image_data=file_data,
            uploaded_by=user,
            location=location  # Thêm thông tin địa điểm
        )
        image.save()
        
        return image
    
    @staticmethod
    def get_all_images(page=1, per_page=20):
        """Lấy tất cả hình ảnh với phân trang"""
        return Image.objects.order_by('-created_at').paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_user_images(user_id, page=1, per_page=20):
        """Lấy tất cả hình ảnh được tải lên bởi một người dùng cụ thể"""
        user = User.objects(id=user_id).first()
        return Image.objects(uploaded_by=user).order_by('-created_at').paginate(page=page, per_page=per_page)
    
    @staticmethod
    def get_image_by_id(image_id):
        """Lấy hình ảnh theo ID"""
        return Image.objects(id=image_id).first()
    
    @staticmethod
    def get_image_data(image_id):
        """Lấy dữ liệu nhị phân của hình ảnh để hiển thị"""
        try:
            from bson.objectid import ObjectId
            
            # Chuyển đổi image_id thành ObjectId
            obj_id = ObjectId(image_id)
            image = Image.objects(id=obj_id).first()
            
            if not image:
                from flask import abort
                return abort(404, description="Không tìm thấy ảnh")
            
            if not hasattr(image, 'image_data') or not image.image_data:
                from flask import abort
                return abort(404, description="Không có dữ liệu ảnh")
            
            # Xác định MIME type
            mimetype = image.content_type if hasattr(image, 'content_type') and image.content_type else 'image/jpeg'
            
            # Sử dụng các tham số cơ bản mà tất cả các phiên bản Flask đều hỗ trợ
            return send_file(
                io.BytesIO(image.image_data),
                mimetype=mimetype,
                as_attachment=False
            )
        except Exception as e:
            # Log lỗi
            import traceback
            print(f"Lỗi khi lấy dữ liệu ảnh: {e}")
            print(traceback.format_exc())
            
            # Trả về lỗi 500
            from flask import abort
            return abort(500, description=f"Lỗi server: {str(e)}")

    
    @staticmethod
    def update_image(image_id, user_id, description):
        """Cập nhật mô tả hình ảnh"""
        image = Image.objects(id=image_id).first()
        user = User.objects(id=user_id).first()
        
        if not image or not user:
            return False
        
        # Kiểm tra xem người dùng có phải là chủ sở hữu của hình ảnh không
        if str(image.uploaded_by.id) != user_id and user.role != 'admin':
            return False
        
        # Cập nhật mô tả
        image.description = description
        image.save()
        return True
    
    @staticmethod
    def delete_image(image_id, user_id):
        """Xóa hình ảnh (người dùng chỉ có thể xóa hình ảnh của họ)"""
        image = Image.objects(id=image_id).first()
        user = User.objects(id=user_id).first()
        
        if not image or not user:
            return False
        
        # Kiểm tra xem người dùng có phải là chủ sở hữu của hình ảnh không
        if str(image.uploaded_by.id) != user_id and user.role != 'admin':
            return False
        
        # Xóa bản ghi hình ảnh (dữ liệu nhị phân cũng sẽ bị xóa)
        image.delete()
        
        return True
    
    @staticmethod
    def admin_delete_image(image_id):
        """Chức năng admin để xóa bất kỳ hình ảnh nào"""
        image = Image.objects(id=image_id).first()
        
        if not image:
            return False
        
        # Xóa bản ghi hình ảnh
        image.delete()
        
        return True