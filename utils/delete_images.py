import cloudinary.api


def delete_images(images: list):
    """
    Elimina imágenes de Cloudinary
    :param images: Lista de public_ids de las imágenes a eliminar
    """
    if images:
        try:
            cloudinary.api.delete_resources(images)
            return True
        except Exception as e:
            print(f"Error al eliminar las imágenes: {e}")
            return False
