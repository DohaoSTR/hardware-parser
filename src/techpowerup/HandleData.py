# запарсить все нужное на этом сайте
# тут нужно отделять значение меры от просто значения и делать это грамотно

from .Part import Part

category = Part.CPU
category_name = Part.PART_LINK_MAPPING[category] 
print(category_name)