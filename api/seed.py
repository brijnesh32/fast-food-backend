from api.models import Category, FoodItem
from api.dummy_data import dummyData
def run_seed():
    if Category.objects.first() or FoodItem.objects.first():
        return
    category_map = {}
    for c in dummyData['categories']:
        obj = Category(name=c['name'], description=c.get('description','')).save()
        category_map[c['name']] = obj
    for m in dummyData['menu']:
        cat = category_map.get(m['category_name'])
        if not cat:
            continue
        FoodItem(name=m['name'], description=m.get('description',''), image_url=m.get('image_url',''), price=m.get('price',0.0), rating=m.get('rating'), calories=m.get('calories'), protein=m.get('protein'), category=cat, customizations=m.get('customizations',[])).save()
    print('Seed completed.')
