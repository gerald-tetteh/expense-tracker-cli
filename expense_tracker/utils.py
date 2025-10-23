import locale
import platform


class Utils:
    """Utility functions for the expense tracker application."""
    month_ordinals = {
        "Jan": "1",
        "Feb": "2",
        "Mar": "3",
        "Apr": "4",
        "May": "5",
        "Jun": "6",
        "Jul": "7",
        "Aug": "8",
        "Sep": "9",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    short_to_full_month_map = {
        "Jan": "January",
        "Feb": "February",
        "Mar": "March",
        "Apr": "April",
        "May": "May",
        "Jun": "June",
        "Jul": "July",
        "Aug": "August",
        "Sep": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }
    categories = {
        "Food & Drinks": [
            "coffee",
            "restaurant",
            "meal",
            "lunch",
            "dinner",
            "breakfast",
            "snack",
            "groceries",
            "supermarket",
            "bar",
            "cafe",
            "beer",
            "wine"
        ],
        "Transport": [
            "uber",
            "lyft",
            "taxi",
            "bus",
            "train",
            "metro",
            "flight",
            "airline",
            "gas",
            "fuel",
            "parking",
            "toll"
        ],
        "Housing & Utilities": [
            "rent",
            "mortgage",
            "electricity",
            "water",
            "internet",
            "wifi",
            "cable",
            "utility",
            "maintenance",
            "repair"
        ],
        "Entertainment": [
            "movie",
            "cinema",
            "netflix",
            "spotify",
            "hbo",
            "concert",
            "game",
            "ticket",
            "streaming",
            "book",
            "music"
        ],
        "Shopping": [
            "amazon",
            "clothes",
            "electronics",
            "shoes",
            "furniture",
            "mall",
            "store",
            "purchase",
            "gift"
        ],
        "Health & Fitness": [
            "gym",
            "fitness",
            "doctor",
            "medicine",
            "pharmacy",
            "dentist",
            "hospital",
            "yoga",
            "vitamin",
            "therapy"
        ],
        "Education": [
            "course",
            "tuition",
            "book",
            "online class",
            "udemy",
            "coursera",
            "university",
            "school",
            "training"
        ],
        "Finance & Fees": [
            "bank",
            "fee",
            "insurance",
            "tax",
            "loan",
            "credit",
            "interest",
            "atm",
            "transfer"
        ],
        "Personal Care": [
            "haircut",
            "salon",
            "barber",
            "spa",
            "cosmetics",
            "beauty",
            "makeup",
            "skincare"
        ],
        "Miscellaneous": [
            "donation",
            "gift",
            "charity",
            "subscription",
            "membership",
            "misc",
            "other"
        ]
    }

    @staticmethod
    def format_currency(amount: float) -> str:
        """
        Format a number as a currency string.

        Args:
            amount (float): The amount to format.
        """
        try:
            loc = locale.getlocale()
            if loc == (None, None):
                if platform.system() == "Windows":
                    locale.setlocale(
                        locale.LC_ALL, "English_United States.1252")
                else:
                    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        except Exception:
            if platform.system() == "Windows":
                locale.setlocale(locale.LC_ALL, "English_United States.1252")
            else:
                locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        try:
            return locale.currency(amount, grouping=True)
        except Exception:
            return f"${amount:,.2f}"

    @staticmethod
    def month_short_to_full(month: str) -> str:
        """
        Returns the full month text.

        Args:
            month (str): Short form of the month
        """
        if month not in Utils.short_to_full_month_map:
            raise ValueError(
                f"Invalid month. Available options: {", ".join(Utils.month_ordinals.keys())}")
        return Utils.short_to_full_month_map[month]

    @staticmethod
    def month_text_to_ordinal(month: str) -> str:
        """
        Returns the ordinal for the months of the year.
        Eg: Jan = 1, Feb = 2.

        Args:
            month (str): Short form of the month
        """
        if month not in Utils.month_ordinals:
            raise ValueError(
                f"Invalid month. Available options: {", ".join(Utils.month_ordinals.keys())}")
        return Utils.month_ordinals[month]

    @staticmethod
    def auto_categorise(description: str) -> str:
        """
        Determine category of expense base on the description

        Args:
            description (str): the expense description
        """
        description_lower = description.lower()
        for key, words in Utils.categories.items():
            if any(word in description_lower for word in words):
                return key
        return "Other"
