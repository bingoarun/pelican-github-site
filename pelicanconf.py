#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Arun prasath'
SITENAME = u'Arun\'s blog'
SITEURL = ''
SITETITLE="Arun prasath"
SITESUBTITLE="Cloud engineer"
SITELOGO="https://avatars2.githubusercontent.com/u/5082801?v=3&s=460"
PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'
MAIN_MENU = True
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = (('Archives', '/archives.html'),
             ('Categories', '/categories.html'),
             ('Tags', '/tags.html'),)

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         )

# Social widget

DEFAULT_PAGINATION = 10
#PAGINATED_DIRECT_TEMPLATES = ('blog-index',)
#DIRECT_TEMPLATES = ('categories', 'index', 'blog-index', 'blog')
THEME= 'Flex'

SOCIAL = (('linkedin', 'http://www.linkedin.com/in/bingoarunprasath'),
          ('github', 'https://github.com/bingoarunprasath'),
          ('facebook','https://www.facebook.com/bingoarunprasath'),
          )
STATIC_PATHS = ['images']
#SITE_THUMBNAIL = 'https://dl.dropboxusercontent.com/u/299446/logo.png'
#SITE_THUMBNAIL_TEXT = 'Cloud tech'
#SITESUBTITLE = 'Cloud sub tech'

#===theme settings===========================

FAVICON = 'images/favicon.jpg'

ROBOTS = 'index, follow'

COPYRIGHT_YEAR = 2016
CC_LICENSE = { 'name': 'bingoarunprasath', 'version':'1.0', 'slug': 'by-sa' }
#ICON = 'https://dl.dropboxusercontent.com/u/299446/logo.png'
#SHORTCUT_ICON = 'https://dl.dropboxusercontent.com/u/299446/logo.png'
#HEADER_IMAGE = 'images/banner.png'
#BACKGROUND_IMAGE = 'https://dl.dropboxusercontent.com/u/299446/logo-invert.png'
# COPYRIGHT = '2015 &copy; All Rights Reserved.'
# Google fonts can be downloaded with
# https://neverpanic.de/downloads/code/2014-03-19-downloading-google-web-fonts-for-local-hosting-fetch.sh'
# Maybe you need to add missing mime types to your webserver configuration
# USER_FONT = '/theme/fonts/font.css'
# USER_BOOTSTRAP = '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4'
# USER_FONTAWESOME = '//maxcdn.bootstrapcdn.com/font-awesome/4.3.0'
# USER_JQUERY = '//code.jquery.com/jquery-1.11.2.min.js'

# About ME
#PERSONAL_PHOTO = "https://scontent.fblr1-1.fna.fbcdn.net/v/t1.0-9/12208620_10205523530628665_1268258118122647299_n.jpg?oh=dfdc4abdc74abbdee204f2cb0e124fcf&oe=57D20623"
#PERSONAL_INFO = """I am Openstack cloud engineer in Wanclouds, currently deployed in Cisco Inc for Openstack operations. After gaining good experience in HP cloud technologies while working with Visolve Inc, I am now focused on Opensource Cloud tools and frameworks. 

#I not only love learning new technologies, but also apply them practically to solve real world problems. I am also a good Python programmer and interested in automating stuffs. 
#My technology stack includes but not limited to Openstack, Python, Puppet, Ansible and Docker."""

# work
#WORK_DESCRIPTION = ''
# items to descripe a work, "type", "cover-image link", "title", "descption", "link"
#WORK_LIST = (('link', 'https://dl.dropboxusercontent.com/u/299446/BT3-Flat.png', 'Ansible-ELK', 'Ansible role for deploying ELK', 'https://github.com/bingoarunprasath/elk'),)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
