import re
import csv
from collections import Counter
import operator

#pre-seeded tags
top_list = {'dynamic': 9529, 'nsdate': 1956, 'sleep': 2100, 'const': 1748, 'windows-ce': 1654, 'mpmovieplayercontroller': 1574,
            'matlab': 18149, 'new-operator': 1206, 'html5-canvas': 1924, 'prototypejs': 2371, 'monodevelop': 1575, 'dell': 2123,
            'replication': 2727, 'browser-compatibility': 1249, 'updates': 1970, 'namespaces': 4378, 'voip': 1696, 'unity3d': 1473,
            'open-source': 6511, 'cmd': 3014, 'upload': 6048, 'rabbitmq': 1349, 'osx-mountain-lion': 1515, 'vector': 6231,
            'nsarray': 2461, 'listview': 13760, 'netbeans': 9151, 'dynamics-crm': 1492, 'category-theory': 1891, 'virtualization': 6897,
            'dual-boot': 1469, 'errors': 2109, 'hide': 1824, 'bittorrent': 1090, 'android-intent': 8238, 'workflow': 5101, 'bdd': 1169,
            'development-environment': 1396, 'metadata': 2639, 'widget': 3643, 'mef': 1425, 'pygtk': 1391, 'javamail': 1330, 'path': 5960,
            'clearcase': 1106, 'visual-studio-2012': 4689, 'itunes': 3153, 'dependencies': 3241, 'indentation': 1911, 'jquery-ajax': 14113,
            'opengraph': 1253, 'replace': 4686, 'unix': 20205, 'mysqldump': 1327, 'printf': 1461, 'parameter-passing': 1435, 'plot': 3576,
            'hard-drive': 9083, 'doctrine2': 3682, 'bundler': 1438, 'backgroundworker': 1513, 'common-lisp': 1417, 'music': 1988, 'dns': 16179,
            'best-practices': 1180, 'annotations': 3955, 'fastcgi': 1639, 'swap': 1234, 'vps': 2628, 'jms': 2301, 'toolbar': 1210, 'phone': 1551,
            'webbrowser': 2627, 'real-time': 1658, 'vpn': 7178, 'blocking': 1152, 'prism': 1670, 'computer-vision': 1903, 'word': 2017,
            'setup': 2054, 'eclipse': 44092, 'jtable': 2830, 'install': 3449, 'jquery-mobile': 10909, 'root': 2221, 'differential-geometry': 3782,
            'scripting': 9180, 'wordpress-theming': 1977, 'smtp': 6118, 'session-variables': 1232, 'titanium': 2124, 'scheduling': 1564,
            'uac': 1509, 'plist': 1946, 'recovery': 1935, 'vertical-alignment': 1798, 'sharepoint': 15701, 'sata': 1416, 'avfoundation': 1409,
            'actionscript': 7238, '.net-3.5': 5399, 'elasticsearch': 1186, 'nhibernate': 14863, 'core-graphics': 2436, 'ds.algorithms': 1855,
            'lan': 2169, 'exchange-2003': 1565, 'calayer': 1202, 'usb-flash-drive': 1783, 'types': 6883, 'windows-update': 1327,
            'e-commerce': 2575, 'complexity': 1428, 'algorithms': 4605, 'ethernet': 2073, 'order': 2243, 'prepared-statement': 1505,
            'metric-spaces': 1803, 'jpeg': 2143, 'syntax-error': 1568, 'keyboard-shortcuts': 5305, 'concurrency': 6587, 'keyboard': 7799,
            'captions': 1183, 'classpath': 1978, 'textbox': 4920, 'cli': 1203, 'img': 1252, 'android-ndk': 3915, 'glassfish': 3568, 'erlang': 3502,
            'clr': 2074, 'split': 3723, 'fragment': 1154, 'refactoring': 3940, 'environment-variables': 3013, 'decorator': 1125, 'grammar': 1132,
            'left-join': 1577, 'fonts': 10228, 'odbc': 2905, 'subquery': 2021, 'hql': 1796, 'timeout': 3869, 'google-analytics': 3702, 'adobe': 3456,
            'interop': 3364, 'functional-programming': 4532, 'android-manifest': 1697, 'mongoid': 2348, 'extract': 1479, 'message': 1362,
            'whitespace': 1445, 'open': 1173, 'sms': 3406, 'functional-analysis': 6044, 'content': 2311, 'generics': 12901, 'ios6': 4999,
            'ado.net': 5460, 'build-process': 1772, 'windows-vista': 8175, 'free': 1184, 'putty': 1879, 'segmentation-fault': 2710, 'md5': 1725,
            'ireport': 1203, 'logging': 13849, 'ckeditor': 2096, 'client-server': 2592, 'activerecord': 10656, 'javafx': 1359, 'openssl': 3842,
            'filter': 5881, 'mvc': 15325, 'complex-analysis': 6957, 'benchmarking': 1568, 'windows-mobile': 3376, 'observablecollection': 1148,
            'backup': 11309, 'render': 1190, 'hook': 1930, 'mingw': 1991, 'customization': 3702, 'neo4j': 1172, 'service': 8140, 'struts': 2620,
            'twisted': 1376, 'visual-studio-2008': 15500, 'visual-studio-2005': 2949, 'lighttpd': 1537, 'remote-desktop': 4560,
            'file-permissions': 2119, 'uinavigationbar': 1692, 'http-headers': 3689, 'tree': 4332, 'project': 2136, 'file-upload': 9409,
            'zend-framework': 15609, 'hacking': 1299, 'treeview': 3379, 'gae-datastore': 2122, 'uiview': 7259, 'build-automation': 1384,
            'websocket': 2623, 'rewrite': 3593, 'discrete-mathematics': 2799, 'angularjs': 3578, 'omniauth': 1102, 'home-networking': 1244,
            'galois-theory': 1116, 'many-to-many': 2538, 'mkmapview': 2310, 'microsoft-metro': 2735, 'visual-studio': 30148, 'uisearchbar': 1092,
            'three.js': 1453, 'transactions': 5005, 'object': 11765, 'line-breaking': 1139, 'perforce': 1163, 'ssl-certificate': 3448,
            'macbook': 1785, 'mstest': 1284, 'webcam': 2001, 'dom': 12360, 'classloader': 1444, 'partition': 1516, 'wildcard': 1264, 'dos': 1432,
            'language-agnostic': 7198, 'xampp': 3047, 'random': 7405, 'html-parsing': 2318, 'syntax': 7498, 'mediawiki': 1381, 'colors': 6573,
            'layout': 10742, 'implementation': 1251, 'menu': 5696, 'career-development': 1383, 'cross-platform': 2887, 'c++0x': 1214,
            'java-ee-6': 1333, 'ldap': 5127, 'folder': 3615, 'ocr': 1363, 'iptables': 5087, 'cryptography': 4173, 'pass-by-reference': 1167,
            'amazon': 1517, 'glassfish-3': 1244, 'report': 2454, 'delete': 5791, 'ienumerable': 1417, 'architecture': 9196, 'release': 1516,
            'network-shares': 1397, 'clickonce': 1772, 'reference': 5803, 'motherboard': 2173, 'testing': 13805, 'jquery-plugins': 9450,
            'analytics': 1299, 'escaping': 3106, 'web-applications': 12147, 'static-libraries': 1490, 'delphi': 21367, 'jquery-validate': 3121,
            'cdn': 1132, 'html5': 31243, 'opengl-es': 7243, 'packages': 2815, 'ssrs-2008': 2325, 'gdi+': 1554, 'sd-card': 1135, 'triggers': 4981,
            'adapter': 1727, 'tfs2010': 3195, 'syntax-highlighting': 1830, 'logic': 5650, 'global-variables': 2086, 'login': 9802, 'com': 6586,
            'highcharts': 2406, 'facebook-opengraph': 1124, 'master-pages': 1945, 'height': 2512, 'kohana': 1630, 'diff': 2526,
            'binomial-coefficients': 1167, 'codeigniter': 18259, 'opencv': 9674, 'union': 1335, 'medical-science': 1136, 'numerical-methods': 2352,
            'tutorials': 1933, 'numpy': 5184, 'containers': 1417, 'website': 6610, 'html5-video': 1793, 'directshow': 1160, 'telnet': 1381,
            'web-hosting': 2274, 'datatable': 4343, 'exception': 13366, 'aix': 1156, 'gnu': 1145, 'air': 5464, 'formatting': 6647,
            'cross-referencing': 1428, 'anchor': 1791, 'visual-studio-2010': 34433, 'project-management': 3277, 'joomla1.5': 1096,
            'data-structures': 8519, 'ip': 6347, 'sas': 1553, 'io': 5250, 'mouse': 3795, 'httprequest': 1386, 'recursion': 7118, 'make': 3466,
            'couchdb': 2494, 'google-apps-script': 2357, 'css-float': 2805, 'extjs4': 3284, 'log4j': 2929, 'vmware-esx': 1145, 'templates': 16900,
            'raid': 5058, 'filenames': 1712, 'symfony-1.4': 1946, 'android-fragments': 3145, 'normalization': 1138, 'jframe': 2289,
            'contextmenu': 1735, 'uisplitviewcontroller': 1175, 'client': 2951, 'gzip': 2446, 'settimeout': 1144, 'asihttprequest': 1256,
            'solaris': 3794, 'dependency-properties': 1093, 'laptop': 5604, 'bandwidth': 1965, 'garbage-collection': 3902, 'visualization': 1492,
            'ms-access-2007': 1969, 'xmlhttprequest': 3083, 'instance': 1375, 'agile': 1940, 'opencl': 1337, 'character': 1894, 'fortran': 1850,
            'tuples': 1401, 'collections': 7355, 'reference-request': 6064, 'save': 2763, 'database-design': 11759, 'casting': 5453,
            'linked-list': 2942, 'sorting': 13541, 'console-application': 1546, 'background': 5668, 'jruby': 1730, 'daemon': 1456, 'zoom': 2221,
            'windows-server-2003': 11317, 'app-store': 3032, 'security': 34499, 'windows-server-2008': 16323, 'delphi-xe2': 1547,
            'form-validation': 2454, 'fancybox': 3029, 'centos': 13523, 'connection-string': 1684, 'facebook-php-sdk': 1483, 'applescript': 2729,
            'comments': 4554, 'jbutton': 1251, 'uml': 2739, 'uigesturerecognizer': 1260, 'internet-connection': 1285, 'geocoding': 1220,
            'localhost': 3044, 'repository': 3392, 'derivatives': 1749, 'post': 10752, 'properties': 6762, 'postgresql': 18471,
            'graphics-card': 2738, 'google-maps': 16319, 'foreign-keys': 2910, 'joomla': 6926, 'wordpress-plugin': 2923, 'azure': 7821,
            'commit': 1116, 'runtime': 2575, 'query-optimization': 2102, 'browser-addons': 1148, 'soa': 1216, 'autohotkey': 1156, 'puzzle': 1308,
            'parsing': 17471, 'rendering': 2244, 'haskell': 11298, 'doctrine': 3701, 'git': 29377, 'gis': 1270, 'compression': 4087,
            'elementary-set-theory': 3680, 'general-topology': 7996, 'transform': 1359, 'class': 18363, 'width': 2379, 'redmine': 1171,
            'wordpress': 30556, 'editor': 3522, 'call': 1757, 'iis7': 10789, 'iis6': 4470, 'httpclient': 1683, 'fork': 1645, 'sqlalchemy': 2692,
            'preg-match': 1917, 'paypal': 4476, 'computational-geometry': 1238, 'notifications': 4196, 'apache-poi': 1396, 'heap': 1853,
            'selenium2': 1241, 'android-linearlayout': 1255, 'arrays': 50055, 'devexpress': 2575, 'compiler-errors': 3922,
            'google-maps-markers': 1122, 'sharepoint-foundation': 2025, 'powershell': 13518, 'youtube-api': 2128, 'passenger': 1338,
            'obfuscation': 1312, 'sql-order-by': 1536, 'outlook-2007': 1277, 'request': 2928, 'jax-rs': 1383, 'full-text-search': 3202,
            'timezone': 3376, 'haml': 1620, 'uipickerview': 1224, 'excel': 24025, 'entity-framework-5': 1208, 'entity-framework-4': 6854,
            'sybase': 1246, 'jenkins': 3524, 'models': 1172, 'jaxb': 3831, 'center': 1136, 'asterisk': 1290, 'update': 2098, 'webserver': 7612,
            'sql': 132465, 'meteor': 1249, 'itext': 1367, 'scala': 15343, 'modules': 1646, 'arch-linux': 1760, 'time': 7925, 'push': 1657,
            'beamer': 3367, 'osx': 51812, 'logarithms': 1200, 'twitter-bootstrap': 6828, 'iterator': 3537, 'macosx': 3508, 'focus': 3429,
            'operating-systems': 1660, 'themes': 4567, 'special-functions': 1279, 'subclass': 1195, 'custom-taxonomy': 2329, 'row': 1776,
            'iis7.5': 1700, 'varnish': 1200, 'flask': 1576, 'graph': 7244, 'flash': 27458, 'jvm': 3585, 'http-post': 1914, 'string': 37802,
            'nsdictionary': 1707, 'switch-statement': 1812, 'join': 9289, 'subprocess': 1494, 'custom-field': 2089, 'jqgrid': 5906, 'gui': 13275,
            'posts': 3221, 'function-pointers': 1241, 'standards': 1796, 'div': 10464, 'nhibernate-mapping': 1909, 'multiprocessing': 1473,
            'application': 10553, 'edittext': 2232, 'restkit': 1157, 'aptana': 1597, 'phpunit': 2214, 'uiscrollview': 5022, 'pinvoke': 1776,
            'port': 3804, 'windows-installer': 2475, '64bit': 2634, 'beautifulsoup': 1467, 'reporting-services': 7045, 'ssis': 4735,
            'iphone-sdk-3.0': 3263, 'boost': 9275, 'transparency': 1842, 'port-forwarding': 1805, 'windows-8': 10949, 'xcode4.5': 1227,
            'xcode4.3': 1279, 'xcode4.2': 2369, 'apache': 26990, 'windows-7': 58487, 'vb.net': 46653, 'title': 1317, 'queue': 2699,
            'navigation': 5154, 'ipc': 1588, 'math-mode': 2969, 'social-networking': 1257, 'android-widget': 4620, 'licensing': 5227,
            'android-actionbar': 1812, 'intellij-idea': 3724, 'regex': 59223, 'httpd': 1817, 'mouseevent': 1698, 'perl': 28641, 'stylesheet': 1680,
            'handler': 1368, 'iphone': 183573, 'msi': 1955, 'memory': 17362, 'scope': 3647, 'diagrams': 1092, 'sectioning': 2232, 'sharing': 1534,
            'automapper': 1307, 'monotouch': 4250, 'oop': 19016, 'ibm': 1220, 'captcha': 1110, 'try-catch': 1787, 'shell-script': 2132,
            'lightbox': 1359, 'entity-framework-4.1': 3171, 'ninject': 1873, 'winforms': 37370, 'iframe': 10026, 'nsmutablearray': 3048,
            'sql-injection': 1326, 'stream': 4247, 'silverlight-3.0': 1756, 'permutations': 1168, 'substring': 1427, 'google-chrome-extension': 4981,
            'uiimagepickercontroller': 1701, 'c++11': 5597, 'simulation': 1229, 'javascript-events': 8486, 'msmq': 1301, 'inheritance': 11135,
            'asmx': 1720, 'ping': 2065, 'threadpool': 1334, 'foreach': 4890, 'xhtml': 5230, 'pdftex': 1374, 'map': 6263, 'outlook-2010': 1148,
            'modal': 1538, 'clone': 2177, 'mac': 11698, 'xorg': 2249, 'aop': 1325, 'date': 13697, 'microsoft-word': 3260, 'data': 8253,
            'compatibility': 2171, 'google-apps': 1468, 'html-lists': 2166, 'entity-framework': 23978, 'capistrano': 1656, 'switch': 2333,
            'structuremap': 1114, 'dojo': 4871, 'webpage': 1273, 'database-connection': 2071, 'power-management': 1551, 'entity': 2263,
            'memory-allocation': 1647, 'group': 1522, 'monitor': 2070, 'menus': 1845, 'asp.net-membership': 2662, 'gtk': 3431, 'coordinates': 1646,
            'uilabel': 2070, 'forms': 30026, 'yaml': 1298, 'window': 3673, 'flex3': 2880, 'flex4': 3627, 'ember.js': 2518, 'error-handling': 5708,
            'views': 2644, 'rake': 2259, 'scaling': 1415, 'remote-access': 2153, 'file-download': 2049, 'webparts': 1360, 'safari': 5518,
            'uitabbarcontroller': 2852, 'permissions': 13341, 'multisite': 1694, 'fql': 1159, 'opera': 1701, 'config': 1262, 'admob': 1571,
            'textview': 2886, 'x11': 1676, 'el': 1115, 'domain': 3928, 'jquery-animate': 2222, 'hyper-v': 2281, 'naming': 1337, 'paging': 1329,
            'task-parallel-library': 1496, 'canvas': 7922, 'jackson': 1452, 'ejb': 2543, 'internet': 5353, 'code-first': 1134, 'formula': 1156,
            'urllib2': 1130, 'fourier-analysis': 1915, 'hibernate': 24880, 'theory': 1115, 'amazon-web-services': 6485, 'ajax': 62239, 'orm': 7341,
            'mysqli': 3364, 'byte': 1876, 'vector-spaces': 1852, 'language': 1322, 'listings': 1435, 'ocaml': 1538, 'yui': 1527,
            'combinatorics': 8662, 'yum': 2032, 'swing': 25872, 'routes': 3358, 'router': 6358, 'exchange-2007': 1631, 'windows-explorer': 2512,
            'lambda': 4633, 'redhat': 3622, 'variables': 13871, 'client-side': 1158, 'nested': 2455, 'itextsharp': 1631, 'wpf-controls': 3112,
            'ios5': 12090, 'ios4': 4581, 'size': 3132, 'modular-arithmetic': 1148, 'yii': 4358, 'constants': 1619, 'nginx': 11889, 'vsto': 2113,
            'progress-bar': 2405, 'pyqt4': 1568, 'copy': 4161, 'png': 2760, 'thumbnails': 1630, 'lucene': 4264, 'applet': 4169, 
            'posix': 1909, 'amazon-s3': 4920, 'zsh': 1988, 'browser': 11742, 'xpath': 8544, 'san': 1158, 'mvvm': 8336, 'image-manipulation': 1291,
            'ant': 7593, 'jquery-selectors': 5655, 'measure-theory': 5032, 'nsurlconnection': 1688, 'facebook-graph-api': 13830, 'cassandra': 2170,
            'conversion': 1944, 'rmi': 1181, 'alias': 1809, 'animation': 11277, 'wcf': 31490, 'performance': 39377, 'probability-theory': 4529,
            'prime-numbers': 1902, 'printer': 1726, 'internet-explorer-9': 3673, 'internet-explorer-8': 6167, 'artificial-intelligence': 2121,
            'buffer': 1987, 'internet-explorer-7': 3626, 'internet-explorer-6': 2015, 'c#-4.0': 14168, 'software-engineering': 1322,
            'mobile-safari': 2019, 'pages': 1669, 'latex': 3352, 'kendo-ui': 1496, 'textarea': 2503, 'microsoft-outlook-2010': 1095,
            'viewmodel': 1565, 'actionscript-3': 27111, 'webbrowser-control': 1877, 'file-management': 1371, 'uitextfield': 2689,
            'android-contentprovider': 1124, 'screen-scraping': 1708, 'nlp': 2101, 'datetime': 12427, 'datagrid': 6367,
            'programming-languages': 5976, 'ip-address': 2298, 'xml': 64157, 'upgrade': 3804, 'macros': 8626, 'jsoup': 1213, 'texture': 1255,
            '32bit-64bit': 1239, 'taxonomy': 1718, 'datatemplate': 1282, 'c#-2.0': 1399, 'nunit': 2706, 'cluster-computing': 1436,
            'uitextview': 1805, 'get': 4083, 'clang': 1260, 'ssl': 13545, 'ssh': 17866, 'ssd': 3209, 'gem': 3394, 'pdf-generation': 2324,
            'android-layout': 14609, 'settings': 2840, 'c++': 199280, 'wiki': 1595, 'kernel': 4777, 'datatables': 1947, 'fullcalendar': 1638,
            'reverse-engineering': 1233, 'closures': 2044, 'add-in': 1429, 'socket.io': 2089, 'seam': 1322, 'javabeans': 1520, 'calendar': 5326,
            'silverlight-4.0': 5865, 'powerpoint': 1290, 'backbone.js': 7679, 'actionscript-2': 1639, 'xetex': 1757, 'access-vba': 1374,
            'label': 2236, 'import': 6092, 'parent': 1276, 'websphere': 2409, 'screen': 3487, 'pthreads': 2749, '.net-4.0': 7010,
            'serialization': 10067, 'installation': 9222, 'richfaces': 2617, 'mono': 4784, 'datagridview': 5940, 'gwt': 13235, 'modal-dialog': 1606,
            'comet': 1124, 'broadcastreceiver': 2183, 'expression': 1646, 'symfony': 1668, 'phpmyadmin': 4388, 'filtering': 1508,
            'sharedpreferences': 1331, 'firewall': 5793, 'osx-lion': 4834, 'nokogiri': 1342, 'search-engine': 1734, 'learning': 2193, 'twig': 1104,
            'encryption': 11417, 'ruby-on-rails-3.1': 5443, 'ruby-on-rails-3.2': 3135, 'exchange-2010': 2600, 'user-accounts': 1882,
            'copy-paste': 1367, 'sitecore': 1429, 'algebraic-geometry': 4706, 'mocking': 3228, 'external': 1609, 'variable-assignment': 1156,
            'ironpython': 1195, 'ruby': 73502, 'protocols': 1613, 'case': 1439, 'tomcat7': 1477, 'fluent-nhibernate': 4355, 'mount': 3226,
            'admin': 2907, 'group-theory': 7272, 'stdout': 1304, 'canon': 1439, 'concatenation': 1513, 'ascii': 1743, 'binary': 4407,
            'group-by': 3429, 'servlets': 11350, 'hostname': 1111, 'locking': 3279, 'command-line-arguments': 1252, 'authentication': 15932,
            'html': 165507, 'arguments': 2487, 'subdomain': 3149, 'sencha-touch': 2913, 'screenshot': 1757, 'cc.complexity-theory': 2310,
            'dynamics-crm-2011': 1670, 'driver': 1623, 'openldap': 1198, 'cakephp-2.0': 1785, 'virtual-machine': 3882, 'android-viewpager': 1507,
            'wpf': 65836, 'crystal-reports': 4837, 'inversion-of-control': 2019, 'undefined': 1291, 'data-mining': 1102, 'table-of-contents': 2209,
            'components': 2387, 'model': 5695, 'modem': 1180, 'compact-framework': 2536, 'nosql': 3436, 'codeigniter-2': 1212, 'radio-button': 2701,
            'rest': 14426, 'bitmap': 4659, 'gdb': 3229, 'cocos2d': 4009, 'mongoose': 1629, 'touch': 2631, 'greasemonkey': 1543,
            'workflow-foundation-4': 1269, 'samba': 3035, 'sql-server-ce': 2295, 'metaprogramming': 1716, 'generator': 1147, 'ruby-on-rails': 116883,
            'd3.js': 2158, 'color': 1527, 'blob': 1576, 'styles': 3524, 'hover': 3110, 'rubygems': 4201, 'rules': 1176, 'moq': 1469,
            'tikz-pgf': 7378, 'grid': 3824, 'enums': 4675, 'jndi': 1129, 'parent-child': 1290, 'silverlight': 26932, 'avaudioplayer': 1142,
            'intel': 1955, 'server': 2492, 'page-breaking': 1101, 'android-listview': 4149, 'asp.net-webforms': 1249, 'blackberry': 9022,
            'jfreechart': 1125, 'output': 1437, 'computer-science': 3277, 'decimal': 1596, 'jquery-ui-dialog': 1328, 'grouping': 1379, 'cisco': 3737,
            'grub': 2029, 'conditional': 1825, 'operating-system': 3636, 'return-value': 1231, 'images': 3954, '2d': 2035, 'rsync': 3126,
            'windows': 98100, 'rpm': 1594, 'kml': 1154, 'redis': 2687, 'commutative-algebra': 3612, 'scrum': 1169, 'assembly': 8580, 'power': 1283,
            'power-supply': 1513, 'compiler': 6958, 'tdd': 3462, 'comparison': 3595, 'package': 2126, 'acl': 1735, 'xna': 4475, 'struts2': 5306,
            'cuda': 4468, 'permalinks': 2013, 'content-type': 1976, 'nullpointerexception': 3023, 'outlook': 5672, 'core-data': 11264,
            'communication': 1562, 'image': 32280, 'google-calendar': 1280, 'pivot': 1486, '.net-2.0': 2404, 'opengl': 11813, 'hex': 2257,
            'emacs': 10469, 'uiwebview': 5453, 'ipv6': 2285, 'liferay': 1805, 'media': 2348, 'windows-server-2008-r2': 7024,
            'package-management': 1299, 'odata': 1133, 'android-asynctask': 3323, 'taskbar': 1468, 'uiimage': 3458, 'activemq': 1283, 'gorm': 1345,
            'prototype': 1472, 'algorithm': 29773, 'embedded': 3553, 'default': 1692, 'asp.net-mvc-3': 34422, 'asp.net-mvc-4': 6558,
            'ioc-container': 1212, 'graph-theory': 5300, 'dvd': 1567, 'embed': 2012, 'wcf-data-services': 1344, 'delphi-7': 1539, 'youtube': 4908,
            'excel-2007': 2289, 'rvm': 2141, 'nagios': 1512, 'content-management-system': 4278, 'objective-c': 133932, 'asynchronous': 7459,
            'firebug': 2118, 'file': 23406, 'facebook-javascript-sdk': 2062, 'ajaxcontroltoolkit': 1517, 'drivers': 4713, 'mathematica': 3216,
            'storage': 4268, 'field': 1412, 'windows-xp': 20193, 'utf-8': 6381, 'type-conversion': 1883, 'openid': 2349, 'javafx-2': 1488,
            'windows-authentication': 1315, 'pear': 1146, 'richtextbox': 1644, 'registry': 3157, 'dropbox': 1713, 'wxwidgets': 1321,
            'microsoft-outlook': 2400, 'remote': 2401, 'wifi': 3301, 'powershell-v2.0': 1267, 'raphael': 1873, 'directory': 4634,
            'collision-detection': 1263, 'resolution': 2154, 'cpu': 4657, 'bytearray': 1793, 'duplicates': 2179, 'drag-and-drop': 4706,
            'openlayers': 1158, 'mp3': 2946, 'sharepoint2010': 6549, 'disk': 1671, 'scp': 1358, 'hashmap': 2658, 'icons': 3984, 'plesk': 1452,
            'wmi': 2299, 'nodes': 1317, 'java-me': 5731, 'global': 1110, 'proof-strategy': 1458, 'emailserver': 1787, 'mpi': 1270,
            'push-notification': 2252, 'lisp': 2895, 'list': 21628, 'mapreduce': 2794, 'google-maps-api-3': 7754, 'domain-driven-design': 2577,
            'glsl': 1526, 'cookies': 9616, 'gridview': 9870, 'webdav': 1245, 'sync': 3126, 'design': 14833, 'plugins': 15560,
            'shared-libraries': 1953, 'listbox': 4093, 'ribbon': 1288, 'sum': 2046, 'version': 2195, 'differential-equations': 4738,
            'memcached': 3234, 'jsf-2': 6221, 'hash': 6762, 'tags': 5022, 'web-security': 1687, 'compilation': 4808, 'hashtable': 1565,
            'equations': 1544, 'vmware-esxi': 2449, 'search': 16901, 'jax-ws': 1991, 'oracle11g': 3553, 'html-agility-pack': 1091,
            'requirejs': 1375, 'eclipse-plugin': 4945, 'emulator': 1759, 'action': 2010, 'options': 1195, 'vim': 14790, 'joomla2.5': 1281,
            'href': 1225, 'linear-algebra': 15457, 'plone': 1702, 'select': 10723, 'orientation': 2019, 'executable': 1664,
            'interface-builder': 3286, 'distinct': 1254, 'playframework-2.0': 2137, 'authorization': 2612, 'android-service': 1315,
            'operators': 2297, 'equipment-recommendation': 1519, 'jsonp': 2032, 'webkit': 4201, 'symfony-2.0': 1703, 'document': 1549,
            'salesforce': 2140, 'jdk': 1147, 'for-loop': 6337, 'autocomplete': 6049, 'mvvm-light': 1209, 'android-market': 1292, 'history': 2694,
            'compare': 2224, 'share': 1533, 'f#': 4964, 'magento': 15082, 'numbers': 3059, 'vmware-workstation': 1299, 'axis2': 1435,
            'virtual-machines': 1834, 'spreadsheet': 1451, 'maps': 3081, 'pygame': 1246, 'machine-learning': 3033, 'csv': 8702,
            'opengl-es-2.0': 1587, 'css': 129107, 'excel-2010': 1121, 'mapping': 3081, 'string-formatting': 1109, 'lazy-loading': 1567,
            'response': 1476, 'pattern-matching': 2143, 'github': 5819, 'postfix': 4598, 'documentation': 5444, 'django': 52030, 'callback': 4400,
            'andengine': 1144, 'nvidia': 2044, 'inline': 1389, 'uninstall': 1628, 'photoshop': 1365, 'checkbox': 5815, 'xmpp': 2536,
            'asp.net-4.0': 1259, 'code-generation': 1950, 'filters': 1570, 'installer': 3875, 'forms-authentication': 2507, 'custom-controls': 2319,
            'log-files': 1174, 'combobox': 5077, 'selenium': 7302, 'compiling': 1227, 'capybara': 1518, 'return': 1992, 'playframework': 4144,
            'timestamp': 2830, 'memory-management': 10241, 'internet-explorer': 21583, 'sharepoint2007': 3279, 'scipy': 1801, 'ms-office': 1945,
            'amazon-ec2': 9365, 'unit-testing': 19166, 'assemblies': 2119, 'cell': 1184, 'refresh': 2240, 'events': 15884, 'web-part': 2726,
            'inequality': 3171, 'innodb': 1928, 'windows-phone': 1412, 'jmeter': 1188, 'microsoft-excel-2010': 1114, 'stored-procedures': 9874,
            'windows-server': 1135, 'crontab': 1322, 'single-sign-on': 1145, 'loops': 11494, 'ftp': 8966, 'sencha': 1646, 'preg-replace': 2190,
            'load': 4105, 'initialization': 2868, 'dotnetnuke': 1421, 'core-animation': 2464, 'localization': 5919, 'linq-to-objects': 1104,
            'proxy': 9179, 'algebraic-topology': 3486, 'bash': 33116, 'definition': 1541, 'unique': 1372, 'drupal': 12895, 'django-forms': 3614,
            'positioning': 3069, 'django-models': 6338, 'kvm-virtualization': 1462, 'complex-numbers': 1906, 'feed': 1502, 'singleton': 3040,
            'ios-simulator': 2279, 'soft-question': 3368, 'probability': 12930, 'encoding': 8167, 'webforms': 4186, 'operator-overloading': 2287,
            'windows-runtime': 2411, 'file-transfer': 1746, 'gpl': 1226, 'razor': 8413, 'script': 8892, 'mediaplayer': 2094, 'mamp': 1201,
            'jetty': 2450, 'weblogic': 2171, 'web-development': 2301, 'gpu': 1782, 'scheme': 2555, 'store': 1172, 'schema': 2627,
            'cross-browser': 3894, 'colorbox': 1287, 'filesystems': 8573, 'tracking': 1276, 'jdbc': 7961, 'translation': 1896, 'tfs': 5574,
            'error-message': 1245, 'jquery': 305614, 'grep': 4440, 'ffmpeg': 4711, 'stl': 6070, '.htaccess': 21022, 'blogs': 1406,
            'horizontal-alignment': 2039, 'gps': 4037, 'debugging': 18936, 'variable-scope': 1188, 'mootools': 2184, 'bitwise': 1196,
            'wysiwyg': 1498, 'jasper-reports': 2956, 'monodroid': 1814, 'null': 4118, 'character-encoding': 5983, 'drop-down-menu': 7427,
            'windows-phone-8': 1943, 'number-theory': 6969, 'windows-phone-7': 17245, 'tinymce': 3257, 'centos5': 1411, 'build': 5946, 'jsf': 14650,
            'vnc': 1797, 'warnings': 2284, 'data.frame': 1563, 'linq-to-xml': 2498, 'virus': 1464, 'jsp': 17012, 'cygwin': 4212,
            'sql-server-2008-r2': 4034, 'services': 1494, 'statistics': 8470, 'selector': 1483, 'exe': 1277, 'mobile': 11147,
            'external-hard-drive': 2056, 'sql-server-2000': 2473, 'caching': 12960, 'physics': 2413, 'microsoft': 3553, 'xcode': 52513,
            'binary-tree': 1410, 'scrollview': 1586, 'node.js': 20280, 'session': 14695, 'find': 4454, 'drupal-modules': 1367, 'box2d': 1479,
            'iis-7.5': 2317, 'parameters': 6022, 'override': 2000, 'asp.net-ajax': 3385, 'columns': 1537, 'xss': 1563, 'notation': 2524,
            'android-camera': 1377, 'express': 3216, 'opensuse': 1457, 'synchronization': 4230, 'xml-parsing': 4546, 'continuous-integration': 3018,
            'abstract-algebra': 10952, 'activity': 6055, 'wireshark': 1297, 'set': 2221, 'unicode': 8383, 'locale': 1763, 'iteration': 1687,
            'core-audio': 1147, 'startup': 2681, 'web-services': 30141, 'internationalization': 5060, 'sed': 5673, 'user-interface': 9124,
            'seo': 4312, 'close': 1114, 'arm': 2410, 'fullscreen': 1646, 'struct': 4897, 'libraries': 1714, 'mutex': 1239, 'uibutton': 3728,
            'ms-access': 12743, 'profiling': 2816, 'imagemagick': 3028, 'xslt': 12785, 'set-theory': 2395, 'microsoft-excel-2007': 1109,
            'javascript': 365623, 'scalability': 1854, 'integration-testing': 1426, 'knockout.js': 4573, 'java-ee': 13579, 'solr': 5876,
            'floats': 1845, 'osx-snow-leopard': 4704, 'multivariable-calculus': 3288, 'hyperlink': 5347, 'arraylist': 4688, 'primary-key': 1575,
            'wireless-networking': 7817, 'pdo': 4636, 'if-statement': 7258, 'connection': 5183, 'context': 2060, 'pdf': 15619, 'pde': 2522,
            'file-io': 7696, 'geolocation': 4178, 'markdown': 1229, 'ruby-on-rails-3': 43166, 'battery': 1332, 'web-config': 4138, 'header': 4880,
            'shutdown': 1487, 'linux': 127606, 'desktop': 2582, 'probability-distributions': 2849, 'sequences-and-series': 7556,
            'facebook-fql': 1563, 'java': 412189, 'swf': 2339, 'extension-methods': 1633, 'special-characters': 1746, 'asymptotics': 1318,
            'asp.net-mvc-routing': 1891, 'data-binding': 10134, 'swt': 2422, 'files': 1419, 'infopath': 2275, 'stochastic-processes': 2439,
            'slideshow': 1708, 'rspec': 5242, 'multidimensional-array': 5783, 'overloading': 1323, 'z-index': 1499, 'ubuntu-9.10': 1232,
            'imap': 2642, 'floating-point': 4205, 'responsive-design': 1814, 'partial-views': 1181, 'batch': 7387, 'optimization': 14304,
            'match': 1233, 'drawable': 1234, 'loop': 1782, 'prolog': 2626, 'malloc': 2081, 'jpa': 10139, 'code-coverage': 1237, 'binding': 7755,
            'facelets': 1185, 'uitableview': 15544, 'skype': 1618, 'signal-processing': 1597, 'updatepanel': 2169, 'network-share': 1385,
            'fedora': 4739, 'webgl': 1357, 'hadoop': 5849, 'coffeescript': 3062, 'jpa-2.0': 1791, 'onclick': 3595, 'sqlite3': 4907,
            'development': 3393, 'passwords': 5113, 'x86': 3350, 'alert': 1483, 'cucumber': 2386, 'user': 3891, 'banach-spaces': 1138, 'tsql': 20544,
            'stack': 2579, 'background-image': 1560, 'task': 1389, 'database': 59799, 'analysis': 7588, 'double': 1949, 'marshalling': 1310,
            'antlr': 1524, 'python-2.7': 5013, 'mysql': 172182, 'elementary-number-theory': 5227, 'alignment': 2393, 'tables': 3922, 'loading': 1489,
            'in-app-purchase': 2296, 'signals': 2020, 'source': 1611, 'location': 2924, 'input': 7091, 'reportviewer': 1137, 'transformation': 1292,
            'associations': 2459, 'format': 3136, 'jstl': 2159, 'integer': 2805, 'plugin-development': 2631, 'activex': 2328,
            'sql-server-2012': 1161, 'manifest': 1252, 'boolean': 2236, 'software-rec': 3401, 'mapkit': 1830, 'terminology': 4437, 'google': 14480,
            'methods': 6903, 'spring': 26995, 'google-api': 2356, 'streaming': 4085, 'wxpython': 2774, 'imageview': 2494, 'bookmarks': 1376,
            'finite-groups': 1823, 'scale': 1257, 'contacts': 1737, 'exec': 1845, 'integration': 4994, 'real-analysis': 14853, 'notepad++': 2309,
            'cgi': 2639, 'telerik': 3770, 'usercontrols': 5903, 'processing': 1262, 'asp.net-web-api': 2655, 'wget': 1916, 'wsdl': 3574,
            'gnome': 2856, 'relational-database': 1963, 'mod-rewrite': 13275, 'symfony1': 2848, 'symfony2': 7367, 'range': 1658, 'datasource': 1545,
            'dialog': 4751, 'messaging': 1112, 'webview': 4928, 'ide': 5528, 'block': 1422, 'delphi-2010': 1205, 'active-directory': 12460,
            'integral': 5171, 'troubleshooting': 2327, 'multiple-monitors': 3100, 'web-crawler': 1649, 'wicket': 1735, 'asp.net-mvc': 57859,
            'spam': 1806, 'vbscript': 5932, 'live': 1234, 'submit': 2225, 'bios': 2322, 'heroku': 7137, 'linux-kernel': 4582, 'https': 7332,
            'httpwebrequest': 3190, 'linq': 29543, 'sdl': 1409, 'line': 1806, 'sdk': 5786, 'groovy': 6287, 'partitioning': 3967,
            'text-processing': 1294, 'file-sharing': 1849, 'android-activity': 2173, 'shortcuts': 1216, 'lyx': 1178, 'accessibility': 1631,
            'char': 2678, 'tomcat6': 1861, 'xslt-1.0': 1094, 'chat': 2090, 'oauth-2.0': 2057, 'nsuserdefaults': 1149, 'curl': 8986, 'cmake': 2358,
            'gnuplot': 1318, 'nas': 1814, 'nat': 2116, 'load-balancing': 3207, 'pandas': 1176, 'arithmetic': 1408, 'llvm': 1278, 'users': 1864,
            'mongodb': 15499, 'printing': 9541, 'polynomials': 3276, 'lucene.net': 1104, 'lens': 1911, 'eval': 1507, 'drupal-views': 1302,
            'linq-to-sql': 11376, 'bibliographies': 1754, 'structure': 1552, 'svn': 19727, 'webdriver': 2377, 'ntfs': 2502,
            'windows-phone-7.1': 1855, 'svg': 5280, 'inner-join': 1206, 'virtualhost': 2715, 'sftp': 2031, 'jpanel': 2004, '2007': 3858,
            'textmate': 1345, 'oracle': 29382, 'selenium-rc': 1193, 'scroll': 3597, 'reverse-proxy': 1942, 'msbuild': 4966, 'microsoft-excel': 6284,
            'ejb-3.0': 1648, 'dependency-injection': 5420, 'json.net': 1410, 'toggle': 1820, 'gd': 1641, 'ggplot2': 2591, 'legal': 1223,
            'go': 1961, 'query': 28931, 'flash-builder': 2297, 'base64': 1950, 'eclipse-rcp': 1969, 'include': 4192, 'junit': 5215,
            'resources': 5253, 'vlc': 1497, 'facebook': 43393, 'matrices': 7036, 'categories': 3033, 'viewstate': 1140, 'mercurial': 6103,
            'button': 10644, 'font-face': 1317, 'sql-server': 74921, 'algebra-precalculus': 7144, 'rack': 1131, 'versioning': 1779,
            'biztalk': 1187, 'asp-classic': 6242, 'elisp': 1879, 'cron': 6244, 'video': 14300, 'download': 5572, 'tortoisesvn': 2944,
            'click': 3371, 'vmware': 3343, 'sql-server-2008': 29743, 'index': 4016, 'html-helper': 1112, 'phonegap': 11372,
            'sql-server-2005': 18812, 'jboss': 5789, 'clipboard': 1708, 'vb6': 5464, 'cordova': 1582, '3d': 5928, 'text-files': 1638,
            'exchange': 5222, 'winapi': 16422, 'drupal-7': 3958, 'drupal-6': 3918, 'spacing': 2991, 'matplotlib': 3552, 'ubuntu': 43002,
            'jquery-ui': 21395, 'openmp': 1167, 'c++-cli': 2880, 'google-chrome': 20408, 'vba': 14490, 'rdp': 1212, 'uikit': 3442, 'shader': 1257,
            'nsstring': 4080, 'adobe-photoshop': 1287, 'automatic-ref-counting': 1990, 'enterprise-library': 1261, 'language-design': 1246,
            'firefox': 21427, 'apple': 4076, 'apt': 1634, 'apk': 1219, 'api': 22037, 'tools': 1140, 'cloud': 2965, 'wix': 3251,
            'castle-windsor': 1804, 'usb': 8028, 'zip': 3630, 'google-app-engine': 18505, 'hudson': 2610, 'nuget': 1159, 'camera': 4346,
            'haproxy': 1131, 'iis': 18552, 'xaml': 15665, 'visibility': 1141, 'data-recovery': 1865, 'scheduled-tasks': 2191, 'cakephp-1.3': 2007,
            'circle': 1345, 'resize': 4371, 'pagination': 4531, 'tableview': 1427, 'this': 1420, 'windows-registry': 1317, 'control': 2423,
            'sqlite': 20741, 'tar': 1773, 'process': 8001, 'sudo': 2135, 'javadoc': 1162, 'event-log': 1210, 'native': 1273, 'gcc': 10776,
            'sip': 1223, 'pyqt': 2530, 'delay': 1334, 'lamp': 1925, 'attachment': 1105, 'uinavigationcontroller': 4653,
            'desktop-application': 1329, 'profile': 1302, 'session-cookies': 1145, 'url-rewriting': 6573, 'google-drive-sdk': 1296,
            'postback': 1810, 'monitoring': 5011, 'bsod': 1223, 'windows-services': 4674, 'bind': 3164, 'grails': 11313, 'element': 1510,
            'object-oriented': 1309, 'thread-safety': 3437, 'osgi': 2014, 'jira': 1166, 'algebraic-number-theory': 1361, 'symbols': 2224,
            'facebook-c#-sdk': 1708, 'jni': 3075, 'directx': 2713, 'paperclip': 1949, 'openvpn': 2156, 'apache2': 27619, 'multithreading': 37619,
            '2010': 6457, 'flex': 22248, 'crash': 5554, 'python': 184928, 'indexing': 4108, 'ms-word': 3579, 'umbraco': 1304, 'rotation': 3780,
            'cakephp': 13882, 'actionbarsherlock': 1648, 'storyboard': 2585, '.net': 162359, 'merge': 4726, 'scrollbar': 2152, 'nfs': 2185,
            'constraints': 1567, 'memory-leaks': 6369, 'maven-plugin': 1096, 'app-config': 1455, 'bluetooth': 4992, 'image-processing': 9843,
            'books': 3588, 'static': 5616, 'cpanel': 2150, 'margins': 1180, 'matrix': 5282, 'command-line': 17475, 'ssas': 1274, 'dhcp': 2746,
            'spring-mvc': 9708, 'math': 12826, 'dictionary': 6404, 'sendmail': 2509, 'delegates': 4809, 'qt-creator': 1255, 'firefox-addon': 3033,
            'header-footer': 1488, 'geometry': 10586, 'cruisecontrol.net': 1246, 'timer': 5134, 'ring-theory': 2762, 'simplexml': 1725,
            'zend-form': 1532, 'xml-schema': 2552, 'sencha-touch-2': 2067, 'maven-3': 1350, 'maven-2': 5136, 'echo': 1490,
            'workflow-foundation': 1121, 'puppet': 1517, 'facebook-connect': 2862, 'abstract-class': 1452, 'flash-cs5': 1245, 'sockets': 17598,
            'management': 1433, 'makefile': 3785, 'system': 2442, 'wrapper': 1165, 'batch-file': 6232, 'widgets': 1588, 'udp': 3576,
            'shell': 22309, 'rsa': 1799, 'lists': 1319, 'slider': 2941, 'fontsize': 1183, 'while-loop': 2340, 'gson': 1134, 'rss': 5324,
            'ipad': 27098, 'network-programming': 4181, 'pointers': 11310, 'jscrollpane': 1271, 'repository-pattern': 1286, 'software-raid': 1164,
            'group-policy': 2606, 'migration': 5097, 'log4net': 1745, 'twitter-api': 3195, 'tabs': 5717, 'linker': 4399, 'excel-vba': 7176,
            'recurrence-relations': 1162, 'border': 1769, 'user-profile': 1193, 'asp.net': 177334, 'worksheet-function': 1164, 'sinatra': 2451,
            'jboss7.x': 1215, 'vimrc': 1152, 'soap': 9261, 'persistence': 2509, 'calculus': 15679, 'freebsd': 3192, 'wpfdatagrid': 1324,
            'automated-tests': 1641, 'awt': 2092, 'awk': 4806, 'device': 1385, 'gallery': 2581, '64-bit': 3572, 'url': 15163, 'thunderbird': 1923,
            'uri': 1840, 'newline': 1482, 'pipe': 2099, 'bibtex': 1879, 'ef-code-first': 3341, 'selection': 1681, 'text': 9575,
            'eclipselink': 1560, 'oauth': 5761, 'css-selectors': 2366, 'redirect': 13338, 'serial-port': 3184, 'cache': 2074, 'jar': 5268,
            'controls': 2678, 'terminal': 7963, 'local': 1385, 'spring-security': 3829, 'field-theory': 1956, 'ubuntu-12.04': 2158,
            'listener': 1603, 'neural-network': 1204, 'db2': 2804, 'scrolling': 3733, 'converter': 1124, 'design-patterns': 14634, 'aes': 1630,
            'qt': 20586, 'asp.net-mvc-2': 9362, 'git-svn': 1189, 'view': 7463, 'openoffice.org': 1341, 'biblatex': 2002, 'frame': 1369,
            'module': 5152, 'freeze': 1886, 'custom-post-types': 5056, 'popup': 3763, 'hbase': 1189, 'gmail': 4449, 'uialertview': 1147,
            'sql-update': 2096, 'dll': 9028, 'lua': 3823, 'g++': 3112, 'routing': 7780, 'query-string': 1807, 'email': 26888, 'qt4': 3873,
            'session-state': 1094, 'lvm': 1588, 'teamcity': 1688, 'zend-framework2': 1307, 'linux-mint': 1425, 'key': 2331, 'configuration': 10961,
            'runtime-error': 1146, 'hyperref': 1680, 'deadlock': 1125, 'tkinter': 2503, 'coldfusion': 6143, 'accordion': 1372, 'arduino': 1698,
            'ubuntu-10.04': 3816, 'representation-theory': 1504, 'attributes': 4843, 'jersey': 2231, 'preprocessor': 1922,
            'deserialization': 1271, 'nstimer': 1145, 'interface': 6398, 'version-control': 9651, 'cxf': 1796, 'event-handling': 4484,
            'table': 13730, 'android-webview': 1843, 'append': 2153, 'iphone-sdk-4.0': 8177, 'charts': 5265, 'devise': 4456, 'json': 43451,
            'uitableviewcell': 6771, 'aggregate-functions': 1173, 'url-routing': 1796, 'c#': 463526, 'route': 1125, 
            'local-storage': 1523, 'controller': 4489, 'graphics': 11198, 'xpages': 1179, 'cvs': 1293, 'cursor': 3226, 'frameworks': 6376,
            'pgfplots': 1890, 'intellisense': 1396, 'rename': 1806, 'vi': 1232, 'squid': 1810, 'uiimageview': 4101, 'hardware': 3771,
            'linq-to-entities': 3808, 'jquery-events': 1192, 'oracle10g': 3791, 'productivity': 1718, 'jsf-2.0': 1874, 'administration': 1701,
            'unity': 1700, 'sharepoint-enterprise': 2495, 'android': 320622, 'http': 19768, 'video-streaming': 2985, 'reporting': 2147,
            'ios': 136080, 'microsoft-office': 1931, 'automation': 5714, 'php': 392451, 'xcode4': 6052, 'polymorphism': 2456, 'coding-style': 5851,
            'reflection': 9197, 'theme-development': 2242, 'draggable': 1477, 'command': 3612, 'position': 2909, 'audio': 14966,
            'parallel-processing': 4278, 'drawing': 2985, 'webclient': 1326, 'wss-3.0': 1149, 'restore': 1945, 'lotus-notes': 1448, 'mfc': 5462,
            'less': 1757, 'oledb': 1534, 'xen': 2034, 'numbering': 1355, 'tcp': 7911, 'tcl': 1570, 'subsonic': 1428, 'xml-serialization': 3209,
            'web': 7491, 'console': 5051, 'exception-handling': 6312, 'spinner': 1701, 'add': 1189, 'adb': 1142, 'facebook-like': 2991,
            'ado': 1280, 'ravendb': 1122, 'homework': 32535, 'primefaces': 4719, 'css3': 13332, 'plsql': 5092, 'wp-query': 1863,
            'bit-manipulation': 1173, 'message-queue': 1091, 'deployment': 10660, 'password': 1488, 'insert': 4810, 'like': 1597, 'xquery': 1341,
            'xsd': 3843, 'xml-rpc': 1121, 'android-mapview': 1751, 'sequence': 1113, 'kde': 1265, 'twitter': 8189, 'export': 3385,
            'overlay': 1947, 'cross-domain': 2531, 'tooltip': 1993, 'django-views': 2124, 'maven': 12482, 'dataannotations': 1256, 'ssms': 1107,
            'document-library': 1701, 'panel': 1455, 'boost-asio': 1302, 'constructor': 5182, 'clojure': 5161, 'uiviewcontroller': 5764,
            'smarty': 1785, 'dataset': 3147, 'cocoa': 26062, 'registration': 1384, 'virtualbox': 6332, 'attachments': 1120, 'media-queries': 1169,
            'networking': 38323, 'snmp': 1547, 'extjs': 9080, 'function': 17967, 'certificate': 3764, 'repeater': 1493, 'dreamweaver': 1505,
            'django-admin': 3336, 'hp': 2299, 'phusion-passenger': 1180, 'godaddy': 1364, 'convergence': 1981, 'overflow': 1805,
            'naming-conventions': 2114, 'count': 4125, 'web-scraping': 1777, 'tomcat': 14848, 'python-3.x': 4930, 'shortcode': 1233,
            'hosting': 4461, 'cocos2d-iphone': 4608, 'big-o': 1130, 'limit': 5566, 'django-templates': 3457, 'cocoa-touch': 26314,
            'distribution': 1214, 'display': 2942, 'datepicker': 3170, 'android-tabhost': 1370, 'links': 2427, 'int': 2234,
            'android-emulator': 5224, 'mime-types': 1312, 'mod-wsgi': 1457, 'education': 1880, 'sprite': 1195, 'visual-c++': 13740,
            'functions': 5730, 'resharper': 1901, 'boot': 6431, 'virtual': 2239, 'branch': 2001, 'php5': 4176, 'kerberos': 1405, 'bundle': 1495,
            'inputstream': 1316, 'cpu-usage': 1653, 'c#-3.0': 2909, 'asset-pipeline': 1325, 'wamp': 2029, 'debian': 12570, 'sphinx': 1292,
            'sass': 1743, 'trigonometry': 4313, 'sharepoint-designer': 3394, 'uitableviewcontroller': 1714, 'flex4.5': 1221,
            'http-status-code-404': 1894, 'source-code': 2034, 'validation': 17713}

minvalue = min(top_list.values())
top_list_count = sum(top_list.values())
#'r': 26863, 'c': 95453

#open training and learn
test_file = open('SampleTrain.csv', "rb")
test_reader = csv.reader(test_file)

true_positive = {}
false_positive = {}
for row in test_reader:
    new_row = [x.lower() for x in row]
    if new_row[0] == 'id':
        continue
    else:
        #look for top words in the row and add
        word_list = ""
        for word in top_list:
            #to add - look for hyphenated attributes 10/17
            if word in new_row[1] or word in new_row[2]:
                word_list += word + " "

    #rate the relevance of the words
    word_count_list= list(word_list.split())
    word_count_dict = {}
    for word in word_count_list:
        if word in top_list:
            #switch to MLE 10/17
            power = top_list[word]*1./top_list_count
            word_count_dict[word]=power
        else:
            power = special[word]*1./top_list_count
            word_count_dict[word]=power
    #sort them in order of relevance
    sorted_word = sorted(word_count_dict.iteritems(), key=operator.itemgetter(1), reverse=True)

    #show the top x values
    break_value = 5
    row_value_list = []
    if len(sorted_word)>=break_value:
        for word in range(break_value):
            row_value_list.append(sorted_word[word][0])
    elif len(sorted_word) > 0 and len(sorted_word)<break_value:
        for word in range(len(sorted_word)):
            row_value_list.append(sorted_word[word][0])  

    #test for true and false positives in row[3]
    for words in row_value_list:
        if words in new_row[3]:
            if words in true_positive:
                true_positive[words] += 1
            else:
                true_positive[words] = 1
        else:
           if words in false_positive:
                false_positive[words] += 1
           else:
                false_positive[words] = 1

test_file.close()

ROC = {}
for words in true_positive:
    if words in false_positive:
        ROC[words] = true_positive[words] * 1. / (true_positive[words] + false_positive[words])
    else:
        ROC[words] = 1

#open the test and push values
train_to_test = open('SampleTest.csv', "rb")
train_to_test_reader = csv.reader(train_to_test)
ofile = open('SampleSubmission.csv', "wb")
writer = csv.writer(ofile, quoting=csv.QUOTE_ALL)
head_tag = ['Id', 'Tags']
writer.writerow(head_tag)

for row in train_to_test_reader:
    new_row = [x.lower() for x in row]
    if new_row[0] == 'id':
        continue
    else:
        #look for top words in the row and add
        word_list = ""
        for word in ROC:
            if (word in new_row[1] and ROC[word] > 0.5) or (word in new_row[2] and ROC[word] > 0.5):
                word_list += word + " " 

    write_row = [new_row[0], word_list]
    writer.writerow(write_row)

train_to_test.close()
ofile.close()
