# запарсить все нужное на этом сайте
# тут нужно отделять значение меры от просто значения и делать это грамотно

from .TechpowerupPart import TechpowerupPart

category = TechpowerupPart.CPU
category_name = TechpowerupPart.PART_LINK_MAPPING[category] 
print(category_name)