#!/usr/bin/env python3
"""
Utility for deriving country and language information from phone numbers
"""

from babel.core import ( get_global,
                         Locale )
from phonenumbers import ( parse as ph_num_parse,
                           region_code_for_number as ph_num_region_code )
from phonenumbers.geocoder import description_for_number as ph_num_description


def get_country_and_language( phone_number : str) -> dict[ str : str] :
    """
    Input:  phone number with or without '+' but with no spaces
    Output: dict with:
        - code_region     : region code
        - code_language   : native language code
        - country_en      : country name in English
        - country_native  : country name in native language
        - language_en     : native language name in English
        - language_native : native language name in its own language
        - US_state        : US state (only for US)
    """
    result = {}
    try :
        # ---------------------------------------------------------------------------------
        # FROM PHONE NUMBERS GET REGION CODE
        # Parse number (add '+' for libphonenumber)
        pn_raw = phone_number if phone_number.startswith("+") else f"+{phone_number}"
        pn_obj = ph_num_parse(pn_raw)
        # ISO territory code (e.g., 'EC', 'ES', 'US')
        code_region = ph_num_region_code(pn_obj)
        if not code_region :
            raise ValueError("Could not determine region from phone number.")
        
        # ---------------------------------------------------------------------------------
        # FROM BABEL GET LANGUAGE CODE
        # Babel get_global data: { 'EC': {'es': {...}, 'qu': {...}}, ... }
        ter_langs      = get_global("territory_languages")
        ter_langs_info = ter_langs.get( code_region, {})
        # Collect languages with official or de-facto flags
        langs = [ ( code, info) for code, info in ter_langs_info.items()
                  if info.get("official_status") in {"official", "de_facto_official" } ]
        # Fallback to listed languages or English
        langs = langs if langs else list(ter_langs_info.items())
        langs = langs if langs else [ ("en",{}) ]
        # Pick the language with the largest population share
        code_lang = max( langs, key = lambda kv :
                         kv[1].get( "population_percent", 0.0) )[0]
        
        # ---------------------------------------------------------------------------------
        # FROM BABEL GET COUNTRY NAME AND LANGUAGE NAME
        # Setup locales
        loc_e = Locale('en')
        loc_n = Locale(code_lang)
        # Get country name
        country_en     = loc_e.territories[code_region]
        country_native = loc_n.territories[code_region]
        # Fallbacks to phone number data
        if not country_en :
            country_en = ph_num_description( pn_obj, "en")
        if not country_native :
            country_native = ph_num_description( pn_obj, code_lang)
        # Get language name
        language_en     = loc_e.languages[code_lang]
        language_native = loc_n.languages[code_lang]
        
        # ---------------------------------------------------------------------------------
        # Prepare result dict
        result = { "code_region"     : code_region,
                   "code_language"   : code_lang,
                   "country_en"      : country_en,
                   "country_native"  : country_native,
                   "language_en"     : language_en,
                   "language_native" : language_native }
        # If region is US then also get state
        if code_region == "US" :
            result["US_state"] = ph_num_description( pn_obj, "en")
    
    except Exception as ex :
        return { "Error in function get_country_and_language" : str(ex) }
    
    return result
