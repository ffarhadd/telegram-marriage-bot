import sqlite3

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from database import create_database


# =========================================================
# مراحل ثبت نام
# =========================================================

GENDER, NAME, AGE, CITY, MARITAL_STATUS, EDUCATION, JOB, HEIGHT, CLOTHING, RELIGION, SECT, ABOUT = range(12)


# =========================================================
# مراحل جستجو
# =========================================================

(
    SEARCH_GENDER,
    SEARCH_AGE,
    SEARCH_CITY,
    SEARCH_MARITAL,
    SEARCH_EDUCATION,
    SEARCH_JOB,
    SEARCH_HEIGHT,
    SEARCH_CLOTHING,
    SEARCH_RELIGION,
    SEARCH_SECT
) = range(12, 22)


# =========================================================
# مراحل ارسال پیام
# =========================================================

CONTACT_MESSAGE = 22


# =========================================================
# شروع ربات
# =========================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["📝 ثبت‌نام"],
        
    ]

    await update.message.reply_text(
        "🌹 به سامانه معرفی ازدواج خوش آمدید 🌹\n\n"
        "این ربات برای کمک به آشنایی افراد جهت ازدواج طراحی شده است.\n\n"
        "برای شروع ابتدا ثبت‌نام کنید و اطلاعات خود را وارد نمایید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )
    
    
    
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📚 راهنمای استفاده از ربات

1️⃣ ثبت‌نام
از منوی اصلی گزینه «📝 ثبت‌نام» را انتخاب کنید و اطلاعات خود را وارد نمایید.

2️⃣ جستجوی همسر
با انتخاب «🔎 جستجوی همسر» می‌توانید معیارهای موردنظر خود را مشخص کنید.

3️⃣ مشاهده پروفایل
از بخش «👤 پروفایل من» اطلاعات ثبت‌شده خود را مشاهده کنید.

4️⃣ درخواست آشنایی
پس از مشاهده پروفایل‌ها می‌توانید برای افراد درخواست آشنایی ارسال کنید.

5️⃣ ویرایش اطلاعات
در صورت تغییر اطلاعات، از گزینه «✏️ ویرایش اطلاعات» استفاده کنید.

برای لغو هر عملیات:
/cancel
را ارسال کنید.
"""

    await update.message.reply_text(text)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🌹 درباره ما

سامانه معرفی ازدواج یک بستر آنلاین برای کمک به آشنایی
افراد دارای قصد ازدواج است.

هدف این سامانه:
✅ ایجاد محیطی ساده و امن برای معرفی افراد
✅ کمک به یافتن گزینه‌های مناسب بر اساس معیارهای انتخابی
✅ حفظ حریم خصوصی کاربران

اطلاعات کاربران فقط برای عملکرد سامانه استفاده می‌شود.
"""

    await update.message.reply_text(text)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
📞 تماس با ما

در صورت داشتن سوال، پیشنهاد یا گزارش مشکل
می‌توانید با پشتیبانی تماس بگیرید.

راه‌های ارتباطی:

📧 ایمیل:
support@example.com

💬 تلگرام:
@YourSupportID

زمان پاسخگویی:
هر روز ۹ صبح تا ۱۸ عصر
"""

    await update.message.reply_text(text)



# =========================================================
# ثبت نام
# =========================================================

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["👨 مرد", "👩 زن"]
    ]

    await update.message.reply_text(
        "لطفاً جنسیت خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["gender"] = update.message.text

    await update.message.reply_text(
        "نام خود را وارد کنید:"
    )

    return NAME


async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    keyboard = [
        ["۱۸ تا ۲۲", "۲۳ تا ۲۷"],
        ["۲۸ تا ۳۲", "۳۳ تا ۳۷"],
        ["۳۸ به بالا"]
    ]

    await update.message.reply_text(
        "سن خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return AGE


async def age(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["age"] = update.message.text

    keyboard = [
        ["تهران", "مشهد"],
        ["اصفهان", "شیراز"],
        ["تبریز", "سایر"]
    ]

    await update.message.reply_text(
        "شهر محل سکونت را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return CITY


async def city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["city"] = update.message.text

    keyboard = [
        ["مجرد"],
        ["مطلقه / مطلق"],
        ["همسر فوت‌شده"]
    ]

    await update.message.reply_text(
        "وضعیت تأهل خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return MARITAL_STATUS


async def marital_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["marital_status"] = update.message.text

    keyboard = [
        ["زیر دیپلم", "دیپلم"],
        ["کاردانی", "کارشناسی"],
        ["کارشناسی ارشد", "دکترا"]
    ]

    await update.message.reply_text(
        "میزان تحصیلات خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return EDUCATION


async def education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["education"] = update.message.text

    keyboard = [
        ["کارمند", "کارگر"],
        ["مهندس", "پزشک"],
        ["معلم", "دانشجو"],
        ["کسب‌وکار آزاد", "خانه‌دار"],
        ["سایر"]
    ]

    await update.message.reply_text(
        "شغل خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return JOB


async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["job"] = update.message.text

    keyboard = [
        ["زیر ۱۵۵", "۱۵۵ تا ۱۶۵"],
        ["۱۶۶ تا ۱۷۵", "۱۷۶ تا ۱۸۵"],
        ["بالاتر از ۱۸۵"]
    ]

    await update.message.reply_text(
        "قد خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return HEIGHT


async def height(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["height"] = update.message.text

    if context.user_data["gender"] == "👩 زن":

        keyboard = [
            ["چادری", "مانتویی"],
            ["اختیاری"]
        ]

        await update.message.reply_text(
            "نوع پوشش خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return CLOTHING

    return await show_registration_religion(update, context)


async def clothing(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["clothing"] = update.message.text

    return await show_registration_religion(update, context)


async def show_registration_religion(update, context):

    keyboard = [
        ["اسلام"],
        ["مسیحیت"],
        ["یهودیت"],
        ["زرتشتی"],
        ["سایر"],
        ["ترجیح می‌دهم پاسخ ندهم"]
    ]

    await update.message.reply_text(
        "دین خود را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return RELIGION


async def religion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["religion"] = update.message.text

    if update.message.text == "اسلام":

        keyboard = [
            ["شیعه", "سنی"],
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"]
        ]

        await update.message.reply_text(
            "مذهب خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SECT

    elif update.message.text == "مسیحیت":

        keyboard = [
            ["کاتولیک"],
            ["ارتدوکس"],
            ["پروتستان"],
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"]
        ]

        await update.message.reply_text(
            "شاخه مسیحیت خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SECT

    elif update.message.text == "یهودیت":

        keyboard = [
            ["ارتدوکس"],
            ["محافظه‌کار"],
            ["اصلاح‌طلب"],
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"]
        ]

        await update.message.reply_text(
            "شاخه یهودیت خود را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SECT

    elif update.message.text == "زرتشتی":

        keyboard = [
            ["زرتشتی"],
            ["ترجیح می‌دهم پاسخ ندهم"]
        ]

        await update.message.reply_text(
            "گزینه مربوط به مذهب را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SECT

    else:

        keyboard = [
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"]
        ]

        await update.message.reply_text(
            "لطفاً گزینه مربوط به مذهب را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SECT


async def sect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["sect"] = update.message.text

    await update.message.reply_text(
        "لطفاً خودتان را در چند جمله معرفی کنید:"
    )

    return ABOUT


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["about"] = update.message.text

    if context.user_data["gender"] == "👨 مرد":
        context.user_data["clothing"] = ""

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO users
        (
            telegram_id,
            gender,
            name,
            age,
            city,
            marital_status,
            education,
            job,
            height,
            clothing,
            religion,
            sect,
            about
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            update.effective_user.id,
            context.user_data["gender"],
            context.user_data["name"],
            context.user_data["age"],
            context.user_data["city"],
            context.user_data["marital_status"],
            context.user_data["education"],
            context.user_data["job"],
            context.user_data["height"],
            context.user_data["clothing"],
            context.user_data["religion"],
            context.user_data["sect"],
            context.user_data["about"]
        )
    )

    connection.commit()
    connection.close()

    keyboard = [
        ["🔎 جستجوی همسر"],
        ["👤 پروفایل من"],
        ["✏️ ویرایش اطلاعات"],
        ["💌 درخواست‌های آشنایی"],
        ["🗑 حذف حساب"]
    ]

    await update.message.reply_text(
        "✅ ثبت‌نام شما با موفقیت انجام شد.\n\n"
        "به منوی اصلی خوش آمدید.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True
        )
    )

    context.user_data.clear()

    return ConversationHandler.END


# =========================================================
# پروفایل من
# =========================================================

async def my_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            gender,
            name,
            age,
            city,
            marital_status,
            education,
            job,
            height,
            clothing,
            religion,
            sect,
            about
        FROM users
        WHERE telegram_id = ?
        """,
        (update.effective_user.id,)
    )

    user = cursor.fetchone()

    connection.close()

    if not user:

        await update.message.reply_text(
            "❌ هنوز ثبت‌نام نکرده‌اید."
        )

        return

    (
        gender,
        name,
        age,
        city,
        marital_status,
        education,
        job,
        height,
        clothing,
        religion,
        sect,
        about
    ) = user

    profile = (
        "👤 پروفایل شما\n"
        "━━━━━━━━━━━━━━\n\n"
        f"👤 نام: {name}\n"
        f"⚧ جنسیت: {gender}\n"
        f"🎂 سن: {age}\n"
        f"📍 شهر: {city}\n"
        f"💍 وضعیت تأهل: {marital_status}\n"
        f"🎓 تحصیلات: {education}\n"
        f"💼 شغل: {job}\n"
        f"📏 قد: {height}\n"
    )

    if gender == "👩 زن":
        profile += f"👗 پوشش: {clothing}\n"

    profile += (
        f"🕌 دین: {religion}\n"
        f"☪️ مذهب / شاخه: {sect}\n\n"
        f"📝 درباره من:\n{about}"
    )

    await update.message.reply_text(profile)



# =========================================================
# ویرایش اطلاعات
# =========================================================

EDIT_FIELD, EDIT_VALUE, EDIT_RELIGION, EDIT_SECT, EDIT_ABOUT = range(22, 27)


async def edit_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        ["⚧ جنسیت", "👤 نام"],
        ["🎂 سن", "📍 شهر"],
        ["💍 وضعیت تأهل", "🎓 تحصیلات"],
        ["💼 شغل", "📏 قد"],
        ["👗 پوشش", "🕌 دین"],
        ["📝 معرفی"],
        ["❌ انصراف"]
    ]

    await update.message.reply_text(
        "✏️ کدام اطلاعات را می‌خواهید ویرایش کنید؟",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return EDIT_FIELD


async def edit_field(update: Update, context: ContextTypes.DEFAULT_TYPE):

    choice = update.message.text

    if choice == "❌ انصراف":
        return await cancel(update, context)

    fields = {
        "⚧ جنسیت": "gender",
        "👤 نام": "name",
        "🎂 سن": "age",
        "📍 شهر": "city",
        "💍 وضعیت تأهل": "marital_status",
        "🎓 تحصیلات": "education",
        "💼 شغل": "job",
        "📏 قد": "height",
        "👗 پوشش": "clothing",
        "🕌 دین": "religion",
        "📝 معرفی": "about"
    }

    if choice not in fields:
        await update.message.reply_text("لطفاً یکی از گزینه‌های منو را انتخاب کنید.")
        return EDIT_FIELD

    field = fields[choice]
    context.user_data["edit_field"] = field

    if field == "gender":
        keyboard = [["👨 مرد", "👩 زن"]]
        await update.message.reply_text(
            "جنسیت جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "name":
        await update.message.reply_text("نام جدید را وارد کنید:")
        return EDIT_VALUE

    if field == "age":
        keyboard = [
            ["۱۸ تا ۲۲", "۲۳ تا ۲۷"],
            ["۲۸ تا ۳۲", "۳۳ تا ۳۷"],
            ["۳۸ به بالا"]
        ]
        await update.message.reply_text(
            "سن جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "city":
        keyboard = [["تهران", "مشهد"], ["اصفهان", "شیراز"], ["تبریز", "سایر"]]
        await update.message.reply_text(
            "شهر جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "marital_status":
        keyboard = [["مجرد"], ["مطلقه / مطلق"], ["همسر فوت‌شده"]]
        await update.message.reply_text(
            "وضعیت تأهل جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "education":
        keyboard = [["زیر دیپلم", "دیپلم"], ["کاردانی", "کارشناسی"], ["کارشناسی ارشد", "دکترا"]]
        await update.message.reply_text(
            "تحصیلات جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "job":
        keyboard = [["کارمند", "کارگر"], ["مهندس", "پزشک"], ["معلم", "دانشجو"], ["کسب‌وکار آزاد", "خانه‌دار"], ["سایر"]]
        await update.message.reply_text(
            "شغل جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "height":
        keyboard = [["زیر ۱۵۵", "۱۵۵ تا ۱۶۵"], ["۱۶۶ تا ۱۷۵", "۱۷۶ تا ۱۸۵"], ["بالاتر از ۱۸۵"]]
        await update.message.reply_text(
            "قد جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "clothing":
        keyboard = [["چادری", "مانتویی"], ["اختیاری"]]
        await update.message.reply_text(
            "نوع پوشش جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_VALUE

    if field == "religion":
        keyboard = [["اسلام"], ["مسیحیت"], ["یهودیت"], ["زرتشتی"], ["سایر"], ["ترجیح می‌دهم پاسخ ندهم"]]
        await update.message.reply_text(
            "دین جدید را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        )
        return EDIT_RELIGION

    if field == "about":
        await update.message.reply_text("معرفی جدید خود را وارد کنید:")
        return EDIT_ABOUT


async def save_edit_value(update: Update, context: ContextTypes.DEFAULT_TYPE):

    field = context.user_data.get("edit_field")
    value = update.message.text

    if field == "gender" and value == "👨 مرد":
        value_to_save = value
    else:
        value_to_save = value

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        f"UPDATE users SET {field} = ? WHERE telegram_id = ?",
        (value_to_save, update.effective_user.id)
    )

    if field == "gender" and value == "👨 مرد":
        cursor.execute(
            "UPDATE users SET clothing = '' WHERE telegram_id = ?",
            (update.effective_user.id,)
        )

    connection.commit()
    connection.close()

    context.user_data.clear()

    keyboard = [
        ["🔎 جستجوی همسر"],
        ["👤 پروفایل من"],
        ["✏️ ویرایش اطلاعات"],
        ["💌 درخواست‌های آشنایی"],
        ["🗑 حذف حساب"]
    ]

    await update.message.reply_text(
        "✅ اطلاعات شما با موفقیت ویرایش شد.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    return ConversationHandler.END


async def edit_religion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["edit_religion"] = update.message.text

    keyboard = []

    if update.message.text == "اسلام":
        keyboard = [["شیعه", "سنی"], ["سایر"], ["ترجیح می‌دهم پاسخ ندهم"]]
    elif update.message.text == "مسیحیت":
        keyboard = [["کاتولیک"], ["ارتدوکس"], ["پروتستان"], ["سایر"], ["ترجیح می‌دهم پاسخ ندهم"]]
    elif update.message.text == "یهودیت":
        keyboard = [["ارتدوکس"], ["محافظه‌کار"], ["اصلاح‌طلب"], ["سایر"], ["ترجیح می‌دهم پاسخ ندهم"]]
    elif update.message.text == "زرتشتی":
        keyboard = [["زرتشتی"], ["ترجیح می‌دهم پاسخ ندهم"]]
    else:
        keyboard = [["سایر"], ["ترجیح می‌دهم پاسخ ندهم"]]

    await update.message.reply_text(
        "شاخه یا مذهب جدید را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )

    return EDIT_SECT


async def edit_sect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    religion_value = context.user_data["edit_religion"]
    sect_value = update.message.text

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET religion = ?, sect = ? WHERE telegram_id = ?",
        (religion_value, sect_value, update.effective_user.id)
    )

    connection.commit()
    connection.close()

    context.user_data.clear()

    keyboard = [
        ["🔎 جستجوی همسر"],
        ["👤 پروفایل من"],
        ["✏️ ویرایش اطلاعات"],
        ["💌 درخواست‌های آشنایی"],
        ["🗑 حذف حساب"]
    ]

    await update.message.reply_text(
        "✅ اطلاعات دین و مذهب شما با موفقیت ویرایش شد.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    return ConversationHandler.END


async def edit_about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE users SET about = ? WHERE telegram_id = ?",
        (update.message.text, update.effective_user.id)
    )

    connection.commit()
    connection.close()

    context.user_data.clear()

    keyboard = [
        ["🔎 جستجوی همسر"],
        ["👤 پروفایل من"],
        ["✏️ ویرایش اطلاعات"],
        ["💌 درخواست‌های آشنایی"],
        ["🗑 حذف حساب"]
    ]

    await update.message.reply_text(
        "✅ معرفی شما با موفقیت ویرایش شد.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

    return ConversationHandler.END


# =========================================================
# لغو
# =========================================================

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ عملیات لغو شد."
    )

    return ConversationHandler.END


edit_conversation = ConversationHandler(

    entry_points=[
        MessageHandler(
            filters.Regex("^✏️ ویرایش اطلاعات$"),
            edit_profile
        )
    ],

    states={
        EDIT_FIELD: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_field)
        ],
        EDIT_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, save_edit_value)
        ],
        EDIT_RELIGION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_religion)
        ],
        EDIT_SECT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_sect)
        ],
        EDIT_ABOUT: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, edit_about)
        ]
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)


# =========================================================
# شروع جستجو
# =========================================================

async def search_partner(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"] = {}

    keyboard = [
        ["👨 مرد", "👩 زن"]
    ]

    await update.message.reply_text(
        "🔎 جستجوی همسر\n\n"
        "به دنبال چه کسی هستید؟",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_GENDER


# =========================================================
# جنسیت جستجو
# =========================================================

async def search_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["gender"] = update.message.text

    keyboard = [
        ["۱۸ تا ۲۲", "۲۳ تا ۲۷"],
        ["۲۸ تا ۳۲", "۳۳ تا ۳۷"],
        ["۳۸ به بالا"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "🎂 سن موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_AGE


# =========================================================
# سن جستجو
# =========================================================

async def search_age(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["age"] = update.message.text

    keyboard = [
        ["تهران", "مشهد"],
        ["اصفهان", "شیراز"],
        ["تبریز", "سایر"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "📍 شهر موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_CITY


# =========================================================
# شهر جستجو
# =========================================================

async def search_city(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["city"] = update.message.text

    keyboard = [
        ["مجرد"],
        ["مطلقه / مطلق"],
        ["همسر فوت‌شده"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "💍 وضعیت تأهل موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_MARITAL


# =========================================================
# وضعیت تأهل جستجو
# =========================================================

async def search_marital(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["marital_status"] = update.message.text

    keyboard = [
        ["زیر دیپلم", "دیپلم"],
        ["کاردانی", "کارشناسی"],
        ["کارشناسی ارشد", "دکترا"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "🎓 تحصیلات موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_EDUCATION


# =========================================================
# تحصیلات جستجو
# =========================================================

async def search_education(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["education"] = update.message.text

    keyboard = [
        ["کارمند", "کارگر"],
        ["مهندس", "پزشک"],
        ["معلم", "دانشجو"],
        ["کسب‌وکار آزاد", "خانه‌دار"],
        ["سایر"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "💼 شغل موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_JOB


# =========================================================
# شغل جستجو
# =========================================================

async def search_job(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["job"] = update.message.text

    keyboard = [
        ["زیر ۱۵۵", "۱۵۵ تا ۱۶۵"],
        ["۱۶۶ تا ۱۷۵", "۱۷۶ تا ۱۸۵"],
        ["بالاتر از ۱۸۵"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "📏 قد موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_HEIGHT


# =========================================================
# قد جستجو
# =========================================================

async def search_height(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["height"] = update.message.text

    if context.user_data["search"]["gender"] == "👩 زن":

        keyboard = [
            ["چادری", "مانتویی"],
            ["اختیاری"],
            ["فرقی ندارد"]
        ]

        await update.message.reply_text(
            "👗 پوشش موردنظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SEARCH_CLOTHING

    return await show_search_religion(update, context)


# =========================================================
# پوشش جستجو
# =========================================================

async def search_clothing(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["clothing"] = update.message.text

    return await show_search_religion(update, context)


async def show_search_religion(update, context):

    keyboard = [
        ["اسلام"],
        ["مسیحیت"],
        ["یهودیت"],
        ["زرتشتی"],
        ["سایر"],
        ["ترجیح می‌دهم پاسخ ندهم"],
        ["فرقی ندارد"]
    ]

    await update.message.reply_text(
        "🕌 دین موردنظر را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

    return SEARCH_RELIGION


# =========================================================
# دین جستجو
# =========================================================

async def search_religion(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["religion"] = update.message.text

    if update.message.text == "فرقی ندارد":

        context.user_data["search"]["sect"] = "فرقی ندارد"

        return await perform_search(update, context)

    if update.message.text == "اسلام":

        keyboard = [
            ["شیعه", "سنی"],
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"],
            ["فرقی ندارد"]
        ]

        await update.message.reply_text(
            "☪️ مذهب موردنظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SEARCH_SECT

    elif update.message.text == "مسیحیت":

        keyboard = [
            ["کاتولیک"],
            ["ارتدوکس"],
            ["پروتستان"],
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"],
            ["فرقی ندارد"]
        ]

        await update.message.reply_text(
            "✝️ شاخه مسیحیت موردنظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SEARCH_SECT

    elif update.message.text == "یهودیت":

        keyboard = [
            ["ارتدوکس"],
            ["محافظه‌کار"],
            ["اصلاح‌طلب"],
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"],
            ["فرقی ندارد"]
        ]

        await update.message.reply_text(
            "✡️ شاخه یهودیت موردنظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SEARCH_SECT

    elif update.message.text == "زرتشتی":

        keyboard = [
            ["زرتشتی"],
            ["ترجیح می‌دهم پاسخ ندهم"],
            ["فرقی ندارد"]
        ]

        await update.message.reply_text(
            "مذهب موردنظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SEARCH_SECT

    else:

        keyboard = [
            ["سایر"],
            ["ترجیح می‌دهم پاسخ ندهم"],
            ["فرقی ندارد"]
        ]

        await update.message.reply_text(
            "مذهب موردنظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return SEARCH_SECT


# =========================================================
# مذهب جستجو
# =========================================================

async def search_sect(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["search"]["sect"] = update.message.text

    return await perform_search(update, context)


# =========================================================
# جستجو در دیتابیس
# =========================================================

async def perform_search(update: Update, context: ContextTypes.DEFAULT_TYPE):

    search = context.user_data["search"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    query = """
        SELECT
            telegram_id,
            gender,
            name,
            age,
            city,
            marital_status,
            education,
            job,
            height,
            clothing,
            religion,
            sect,
            about
        FROM users
        WHERE telegram_id != ?
    """

    parameters = [update.effective_user.id]

    if search["gender"] != "فرقی ندارد":
        query += " AND gender = ?"
        parameters.append(search["gender"])

    if search["age"] != "فرقی ندارد":
        query += " AND age = ?"
        parameters.append(search["age"])

    if search["city"] != "فرقی ندارد":
        query += " AND city = ?"
        parameters.append(search["city"])

    if search["marital_status"] != "فرقی ندارد":
        query += " AND marital_status = ?"
        parameters.append(search["marital_status"])

    if search["education"] != "فرقی ندارد":
        query += " AND education = ?"
        parameters.append(search["education"])

    if search["job"] != "فرقی ندارد":
        query += " AND job = ?"
        parameters.append(search["job"])

    if search["height"] != "فرقی ندارد":
        query += " AND height = ?"
        parameters.append(search["height"])

    if search["gender"] == "👩 زن":
        if search.get("clothing") != "فرقی ندارد":
            query += " AND clothing = ?"
            parameters.append(search["clothing"])

    if search["religion"] != "فرقی ندارد":
        query += " AND religion = ?"
        parameters.append(search["religion"])

    if search.get("sect") != "فرقی ندارد":
        query += " AND sect = ?"
        parameters.append(search["sect"])

    query += " LIMIT 20"

    cursor.execute(query, parameters)
    users = cursor.fetchall()
    connection.close()

    context.user_data.pop("search", None)
    context.user_data["search_results"] = {}

    if not users:
        await update.message.reply_text(
            "😔 موردی با این مشخصات پیدا نشد."
        )
        return ConversationHandler.END

    await update.message.reply_text(
        f"🔎 تعداد {len(users)} مورد مطابق معیارهای شما پیدا شد."
    )

    for index, user in enumerate(users, start=1):

        (
            target_telegram_id,
            gender,
            name,
            age,
            city,
            marital_status,
            education,
            job,
            height,
            clothing,
            religion,
            sect,
            about
        ) = user

        context.user_data["search_results"][str(index)] = target_telegram_id

        profile = (
            f"👤 مورد شماره {index}\n"
            f"━━━━━━━━━━━━━━\n\n"
            f"👤 نام: {name}\n"
            f"⚧ جنسیت: {gender}\n"
            f"🎂 سن: {age}\n"
            f"📍 شهر: {city}\n"
            f"💍 وضعیت تأهل: {marital_status}\n"
            f"🎓 تحصیلات: {education}\n"
            f"💼 شغل: {job}\n"
            f"📏 قد: {height}\n"
        )

        if gender == "👩 زن":
            profile += f"👗 پوشش: {clothing}\n"

        profile += (
            f"🕌 دین: {religion}\n"
            f"☪️ مذهب / شاخه: {sect}\n\n"
            f"📝 درباره:\n{about}"
        )

        keyboard = [[
            InlineKeyboardButton(
                "💌 ارسال پیام",
                callback_data=f"contact:{index}"
            )
        ]]

        await update.message.reply_text(
            profile,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    await update.message.reply_text(
        "✅ جستجو به پایان رسید.\n\n"
        "برای ارسال پیام، روی دکمه «💌 ارسال پیام» زیر پروفایل موردنظر بزنید."
    )

    return ConversationHandler.END


# =========================================================
# ارسال پیام به صاحب پروفایل
# =========================================================

async def start_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    result_number = query.data.split(":", 1)[1]
    search_results = context.user_data.get("search_results", {})
    target_telegram_id = search_results.get(result_number)

    if target_telegram_id is None:
        await query.message.reply_text(
            "⚠️ این نتیجه جستجو دیگر در دسترس نیست. لطفاً دوباره جستجو کنید."
        )
        return ConversationHandler.END

    context.user_data["contact_target"] = target_telegram_id

    await query.message.reply_text(
        "💌 پیام خود را برای این شخص بنویسید.\n\n"
        "پیام شما بدون نمایش شناسه تلگرام ارسال خواهد شد."
    )

    return CONTACT_MESSAGE


async def send_contact_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message.text.strip()
    target_telegram_id = context.user_data.get("contact_target")

    if not message:
        await update.message.reply_text(
            "⚠️ لطفاً متن پیام را بنویسید."
        )
        return CONTACT_MESSAGE

    if target_telegram_id is None:
        await update.message.reply_text(
            "⚠️ مقصد پیام پیدا نشد. لطفاً دوباره جستجو کنید."
        )
        return ConversationHandler.END

    try:
        await context.bot.send_message(
            chat_id=target_telegram_id,
            text=(
                "💌 یک پیام آشنایی جدید برای شما ارسال شده است.\n\n"
                f"{message}"
            )
        )

        await update.message.reply_text(
            "✅ پیام شما با موفقیت ارسال شد."
        )

    except Exception:
        await update.message.reply_text(
            "⚠️ ارسال پیام انجام نشد. ممکن است این کاربر ربات را متوقف کرده باشد."
        )

    context.user_data.pop("contact_target", None)
    return ConversationHandler.END


# =========================================================
# ساخت دیتابیس
# =========================================================

create_database()


# =========================================================
# ساخت ربات
# =========================================================

app = Application.builder().token("8528698907:AAFhVGmd_PAqAmhS2yvGD65eseXHbFfOVQ0").build()


# =========================================================
# ثبت نام
# =========================================================

registration_conversation = ConversationHandler(

    entry_points=[
        MessageHandler(
            filters.Regex("^📝 ثبت‌نام$"),
            register
        )
    ],

    states={

        GENDER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                gender
            )
        ],

        NAME: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                name
            )
        ],

        AGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                age
            )
        ],

        CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                city
            )
        ],

        MARITAL_STATUS: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                marital_status
            )
        ],

        EDUCATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                education
            )
        ],

        JOB: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                job
            )
        ],

        HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                height
            )
        ],

        CLOTHING: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                clothing
            )
        ],

        RELIGION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                religion
            )
        ],

        SECT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                sect
            )
        ],

        ABOUT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                about
            )
        ]
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)


# =========================================================
# جستجو
# =========================================================

search_conversation = ConversationHandler(

    entry_points=[
        MessageHandler(
            filters.Regex("^🔎 جستجوی همسر$"),
            search_partner
        )
    ],

    states={

        SEARCH_GENDER: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_gender
            )
        ],

        SEARCH_AGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_age
            )
        ],

        SEARCH_CITY: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_city
            )
        ],

        SEARCH_MARITAL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_marital
            )
        ],

        SEARCH_EDUCATION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_education
            )
        ],

        SEARCH_JOB: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_job
            )
        ],

        SEARCH_HEIGHT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_height
            )
        ],

        SEARCH_CLOTHING: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_clothing
            )
        ],

        SEARCH_RELIGION: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_religion
            )
        ],

        SEARCH_SECT: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                search_sect
            )
        ]
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ]
)


# =========================================================
# گفت‌وگوی ارسال پیام
# =========================================================

contact_conversation = ConversationHandler(

    entry_points=[
        CallbackQueryHandler(
            start_contact,
            pattern=r"^contact:\d+$"
        )
    ],

    states={
        CONTACT_MESSAGE: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                send_contact_message
            )
        ]
    },

    fallbacks=[
        CommandHandler("cancel", cancel)
    ],
    per_message=False
)


# =========================================================
# Handler ها
# =========================================================

app.add_handler(
    CommandHandler("start", start)
)

app.add_handler(
    CommandHandler("help", help_command)
)


app.add_handler(
    CommandHandler("about", about_command)
)


app.add_handler(
    CommandHandler("contact", contact_command)
)


app.add_handler(
    registration_conversation
)

app.add_handler(
    edit_conversation
)

app.add_handler(
    search_conversation
)

app.add_handler(
    contact_conversation
)

app.add_handler(
    MessageHandler(
        filters.Regex("^👤 پروفایل من$"),
        my_profile
    )
)


# =========================================================
# اجرای ربات
# =========================================================

app.run_polling()