from .autentication import autentication
from .login_tester import loginTester

from .main.main_general import mainPanel
from .main.main_escalas import mainEscalas
from .main.main_rata import mainRata
from .main.main_cata import mainCata
from .main.main_flash import mainFlash
from .main.main_sort import mainSort



from .sessions_management.session_details import sessionDetails
from .sessions_management.session_monitor import sessionMonitor

from .sessions_management.sessions_list import sesionsList
from .sessions_management.sessions_list_scales import sesionsListScales
from .sessions_management.sessions_list_rata import sesionsListRata
from .sessions_management.sessions_list_cata import sesionsListCata
from .sessions_management.sessions_list_flash import sesionsListFlash
from .sessions_management.sessions_list_sort import sesionsListSort



from .sessions_config.seleccion_tecnica import selecionTecnica
from .sessions_config.configuration_panel_basic import configurationPanelBasic
from .sessions_config.configuration_panel_tags import configurationPanelTags
from .sessions_config.configuration_panel_codes import configurationPanelCodes
from .sessions_config.configuration_panel_words import configurationPanelWords
from .sessions_config.create_session import createSession

from .tester_management.tester_menu import testerMenu
from .tester_management.tester_create import testerCreate
from .tester_management.tester_search import testerSearch
from .tester_management.tester_list import testerList

from .vocabulary_management.vocabulry_menu import vocabularyMenu
from .vocabulary_management.create_vocabulary import createVocabulary
from .vocabulary_management.view_vocabulary import viewVocabulary
from .vocabulary_management.list_vocabulary import listVocabulary

from .apis.api_tag import newTag
from .apis.api_words import words
from .apis.api_words import wordsVocabulary
from .apis.api_list_words_pf import apiListWordsPF
from .apis.rating_word_scales import ratingWordScales
from .apis.rating_word_cata import ratingWordCata
from .apis.rating_sort import ratingSort
from .apis.rating_napping import ratingNapping
from .apis.user_activity_api import UserActivityApi

from .tester_forms.init_tester_form import initTesterForm
from .tester_forms.panel_main_tester import mainPanelTester
from .tester_forms.subscribe_session import subscribeSessionTester
from .tester_forms.sessions_list_tester import sessionsListTester
from .tester_forms.convencional_scales import convencionalScales
from .tester_forms.cata_test import cataTest
from .tester_forms.pf_test import pfTest
from .tester_forms.sort_test import sortTest
from .tester_forms.napping_test import nappingTest
from .tester_forms.perfil_ideal_phases import perfilIdealPhase1, perfilIdealPhase2, ratingPerfilIdealPhase1, ratingPerfilIdealPhase2
