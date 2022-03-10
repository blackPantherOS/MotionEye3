# Copyright (c) 2022 blackPanther Europe (www.blackpanther.hu)
# Copyright (c) 2013 Calin Crisan
# This file is part of motionEye3.
#
# motionEye is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 

import gettext
gettext.install("messages", "./lang")
_ = gettext.gettext

import locale
import logging

from jinja2 import Environment, FileSystemLoader
from jinja2 import evalcontextfilter, Markup
import settings
import utils

_jinja_env = None

# Translations for templates
from babel.support import Translations
locale_dir = "./lang"
msgdomain = "messages"
default_fallback = 'en_US'
system_lang = locale.getlocale()[0]
extensions = ['jinja2.ext.i18n', 'jinja2.ext.autoescape', 'jinja2.ext.with_']
translations = Translations.load(locale_dir, system_lang)
#loader = FileSystemLoader("templates")


def _init_jinja():
    global _jinja_env

    _jinja_env = Environment(extensions=extensions,
            loader=FileSystemLoader(settings.TEMPLATE_PATH),
            trim_blocks=False)

    _jinja_env.install_gettext_translations(translations)

    logging.info(_('load : %s langs: %s') % (translations, system_lang))

    # globals
    _jinja_env.globals['settings'] = settings

    # filters
    _jinja_env.filters['pretty_date_time'] = utils.pretty_date_time
    _jinja_env.filters['pretty_date'] = utils.pretty_date
    _jinja_env.filters['pretty_time'] = utils.pretty_time
    _jinja_env.filters['pretty_duration'] = utils.pretty_duration

#@_jinja_env.template_filter()
@evalcontextfilter
def generate_string(eval_ctx, localized_value):
    if localized_value is None:
        return ""
    else:
        return Markup("\"" + localized_value + "\"").unescape()

def add_template_path(path):
    global _jinja_env
    if _jinja_env is None:
        _init_jinja()
    
    _jinja_env.loader.searchpath.append(path)


def add_context(name, value):
    global _jinja_env
    if _jinja_env is None:
        _init_jinja()

    _jinja_env.globals[name] = value


def render(template_name, **context):
    global _jinja_env
    if _jinja_env is None:
        _init_jinja()

    template = _jinja_env.get_template(template_name)
    return template.render(**context)
