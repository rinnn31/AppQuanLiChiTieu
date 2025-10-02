# TRANSACTION TYPE VALUES
INCOME_TYPE = 0
EXPENSE_TYPE = 1

# TRANSACTION CATEGORIES FOR EXPENSE AND INCOME
OTHER_CATEGORY = "Khác"

ENTERTAINMENT_CATEGORY = "Giải trí"
FOOD_CATEGORY = "Ăn uống"
TRANSPORT_CATEGORY = "Di chuyển"
CLOTHES_CATEGORY = "Quần áo"
EDUCATION_CATEGORY = "Giáo dục"
MEDICAL_CATEGORY = "Y tế"
COSMETIC_CATEGORY = "Mỹ phẩm"
HOUSEHOLD_CATEGORY = "Gia đình"
TRAVEL_CATEGORY = "Du lịch"
EXPENSE_CATEGORIES = [ENTERTAINMENT_CATEGORY, FOOD_CATEGORY, TRANSPORT_CATEGORY, CLOTHES_CATEGORY, EDUCATION_CATEGORY, MEDICAL_CATEGORY, COSMETIC_CATEGORY, HOUSEHOLD_CATEGORY, OTHER_CATEGORY]

SALARY_CATEGORY = "Lương"
ALLOWANCE_CATEGORY = "Trợ cấp"
INVESTMENT_CATEGORY = "Đầu tư"
BUSINESS_CATEGORY = "Kinh doanh"
GIFT_CATEGORY = "Quà tặng"
INCOME_CATEGORIES = [SALARY_CATEGORY, ALLOWANCE_CATEGORY, INVESTMENT_CATEGORY, BUSINESS_CATEGORY, GIFT_CATEGORY, OTHER_CATEGORY]

__ICON_MAPPING = {
    ENTERTAINMENT_CATEGORY: ":/resources/images/entertainment.png",
    FOOD_CATEGORY: ":/resources/images/food.png",
    TRANSPORT_CATEGORY: ":/resources/images/transport.png",
    CLOTHES_CATEGORY: ":/resources/images/clothes.png",
    EDUCATION_CATEGORY: ":/resources/images/education.png",
    MEDICAL_CATEGORY: ":/resources/images/medical.png",
    COSMETIC_CATEGORY: ":/resources/images/cosmetic.png",
    HOUSEHOLD_CATEGORY: ":/resources/images/household.png",
    OTHER_CATEGORY: ":/resources/images/other.png",
    SALARY_CATEGORY: ":/resources/images/salary.png",
    ALLOWANCE_CATEGORY: ":/resources/images/allowance.png",
    INVESTMENT_CATEGORY: ":/resources/images/investment.png",
    BUSINESS_CATEGORY: ":/resources/images/business.png",
    GIFT_CATEGORY: ":/resources/images/gift.png",
}

__CATEGORY_MAIN_COLOR_MAPPING = {
    ENTERTAINMENT_CATEGORY: "#009F9C",
    FOOD_CATEGORY: "#2600FF",       
    TRANSPORT_CATEGORY: "#2F8DFF",
    CLOTHES_CATEGORY: "#00A043",
    EDUCATION_CATEGORY: "#FF7300",
    MEDICAL_CATEGORY: "#C00000",
    COSMETIC_CATEGORY: "#610000",
    HOUSEHOLD_CATEGORY: "#EDE900",
    TRAVEL_CATEGORY: "#9C00DF",
    OTHER_CATEGORY: "#98CB00",
    SALARY_CATEGORY: "#059D00",
    ALLOWANCE_CATEGORY: "#0984E3",
    INVESTMENT_CATEGORY: "#6C5CE7",
    BUSINESS_CATEGORY: "#D63031",
    GIFT_CATEGORY: "#E17055",
}

__CATEGORY_SUB_COLOR_MAPPING = {
    ENTERTAINMENT_CATEGORY: "#92BFD6",
    FOOD_CATEGORY: "#B3A9FF",       
    TRANSPORT_CATEGORY: "#B0D2E9",
    CLOTHES_CATEGORY: "#BAFFB3",
    EDUCATION_CATEGORY: "#FFD697",
    MEDICAL_CATEGORY: "#FFACAC",
    COSMETIC_CATEGORY: "#C78B8B",
    HOUSEHOLD_CATEGORY: "#FFFEB4",
    OTHER_CATEGORY: "#EFFFC4",
    SALARY_CATEGORY: "#BCFCB1",
    ALLOWANCE_CATEGORY: "#ABDDFF",
    INVESTMENT_CATEGORY: "#CEB6FF",
    BUSINESS_CATEGORY: "#FF9BB1",
    GIFT_CATEGORY: "#FFDCAA",
}

def getIconForCategory(category):
    return __ICON_MAPPING.get(category, ":/resources/images/other.png")

def getSubColorForCategory(category):
    return __CATEGORY_SUB_COLOR_MAPPING.get(category, "#CCCCCC")

def getMainColorForCategory(category):
    return __CATEGORY_MAIN_COLOR_MAPPING.get(category, "#CCCCCC")

def getColorForType(transaction_type : int):
    type_color_mapping = {
        0: "#4BC0C0",
        1: "#FF6384",
    }
    return type_color_mapping.get(transaction_type, "#CCCCCC")  