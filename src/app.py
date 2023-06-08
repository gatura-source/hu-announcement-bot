import logging

from . import utils
from .config import DB_STRING
from .mongo import DepartmentDatabase, UserDatabase
from .scraper import *

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()

# Locale
TRANSLATION_UNIT = utils.create_translation_unit()
LOCALE_DEPARTMENT_MAP = utils.create_locale_department_unit()

# Database objects
DEPARTMENT_DB = DepartmentDatabase(DB_STRING)
USER_DB = UserDatabase(DB_STRING)

# Department initialization
AVAILABLE_DEPARTMENTS: list[BaseDepartment] = \
    [
        CS('hu-cs', 'http://www.cs.hacettepe.edu.tr'),
        SKSDB('hu-sksdb', 'http://www.sksdb.hacettepe.edu.tr/bidbnew/index.php'),
        IE('hu-ie', 'http://www.ie.hacettepe.edu.tr'),
        Mat('hu-mat', 'http://www.mat.hacettepe.edu.tr'),
        BBY('hu-bby', 'http://bby.hacettepe.edu.tr'),
        EE('hu-ee', 'http://www.ee.hacettepe.edu.tr'),
        Phys('hu-phys', 'http://www.phys.hacettepe.edu.tr'),
        Edebiyat('hu-edebiyat', 'http://www.edebiyat.hacettepe.edu.tr'),
        ABOfisi('hu-abofisi', 'https://abofisi.hacettepe.edu.tr'),
        BIDB('hu-bidb', 'http://bidb.hacettepe.edu.tr'),
        JeoMuh('hu-jeomuh', 'https://jeomuh.hacettepe.edu.tr'),
        Hidro('hu-hidro', 'http://www.hidro.hacettepe.edu.tr'),
        BaseDepartment('hu-me', 'http://www.me.hacettepe.edu.tr'),
        BaseDepartment('hu-cheng', 'http://www.cheng.hacettepe.edu.tr'),
        BaseDepartment('hu-bilisim', 'http://www.bilisim.hacettepe.edu.tr'),
        BaseDepartment('hu-muhfak', 'http://www.muhfak.hacettepe.edu.tr'),
        BaseDepartment('hu-chem', 'http://www.chem.hacettepe.edu.tr'),
        BaseDepartment('hu-tomer', 'http://www.tomer.hacettepe.edu.tr'),
        BaseDepartment('hu-tip', 'http://www.tip.hacettepe.edu.tr'),
        BaseDepartment('hu-stat', 'http://www.stat.hacettepe.edu.tr/tr'),
        BaseDepartment('hu-ydyo', 'http://www.ydyo.hacettepe.edu.tr'),
        BaseDepartment('hu-oidb', 'http://www.oidb.hacettepe.edu.tr'),
        BaseDepartment('hu-hukukfakultesi', 'http://www.hukukfakultesi.hacettepe.edu.tr'),
        BaseDepartment('hu-dis', 'http://www.dis.hacettepe.edu.tr'),
        BaseDepartment('hu-adk', 'http://adk.hacettepe.edu.tr'),
        BaseDepartment('hu-iibf', 'http://www.iibf.hacettepe.edu.tr'),
        BaseDepartment('hu-sbky', 'http://www.sbky.hacettepe.edu.tr'),
        BaseDepartment('hu-eczacilik', 'http://www.eczacilik.hacettepe.edu.tr'),
        BaseDepartment('hu-ce', 'http://www.ce.hacettepe.edu.tr'),
        BaseDepartment('hu-cevre', 'http://www.cevre.hacettepe.edu.tr'),
        BaseDepartment('hu-psikoloji', 'http://www.psikoloji.hacettepe.edu.tr'),
        BaseDepartment('hu-egitim', 'http://www.egitim.hacettepe.edu.tr'),
        BaseDepartment('hu-ergoterapi', 'http://www.ergoterapi.hacettepe.edu.tr'),
        BaseDepartment('hu-geomatik', 'http://geomatik.hacettepe.edu.tr'),
        BaseDepartment('hu-food', 'https://food.hacettepe.edu.tr'),
        BaseDepartment('hu-maden', 'https://maden.hacettepe.edu.tr'),
        BaseDepartment('hu-nuke', 'https://nuke.hacettepe.edu.tr'),
        BaseDepartment('hu-ofmamat', 'https://ofmamat.hacettepe.edu.tr'),
        BaseDepartment('hu-imo', 'http://imo.hacettepe.edu.tr'),
        BaseDepartment('hu-bdb', 'http://bdb.hacettepe.edu.tr'),
        BaseDepartment('hu-hemsirelik', 'https://hemsirelik.hacettepe.edu.tr'),
        BaseDepartment('hu-eob', 'https://eob.hacettepe.edu.tr'),
        BaseDepartment('hu-shmyo', 'https://shmyo.hacettepe.edu.tr'),
        BaseDepartment('hu-sbmy', 'https://sbmy.hacettepe.edu.tr'),
        BaseDepartment('hu-baskentosbtbmyo', 'https://baskentosbtbmyo.hacettepe.edu.tr'),
        BaseDepartment('hu-secmeli', 'https://secmeli.hacettepe.edu.tr'),
        BaseDepartment('hu-sosyalbilimler', 'https://sosyalbilimler.hacettepe.edu.tr')
    ]


def decode(text_id: str, language: str) -> str:
    return TRANSLATION_UNIT[language][text_id]


def get_possible_deps(_list) -> list[str]:
    return [dep.id for dep in AVAILABLE_DEPARTMENTS if dep.id not in _list]