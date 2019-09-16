from .ru_locale_manager import RuLocaleManager as RuLocale

def get_locale(key : str):
	if key == 'ru':
		return RuLocale()