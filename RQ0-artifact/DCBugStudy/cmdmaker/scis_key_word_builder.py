from nltk.stem.porter import PorterStemmer
import json


def word_stemmer(word):
    porter_stemmer = PorterStemmer()
    return porter_stemmer.stem(word)
    pass


def type_lib_build():
    # construct type dict
    type_dict = {'configuration-issue': ['link', 'build', 'plugin', 'jdk', 'jre', 'xml', 'config', 'integrate',
                                         'artifact', 'deployment', 'configuration', 'dependency', 'manifest',
                                         'version', 'Struts', 'Document', 'upgrade', 'XercesC',  'compile',
                                         'ant', 'Java', 'classpath', 'java', 'Visual', 'Studio', 'Tomcat',
                                         'Linux', 'Microsoft', 'Apache', 'jar', 'path', 'directory', 'mail',
                                         'installation', 'Solaris', 'libraries', 'Windows', 'OpenSSL', 'Browser',
                                         'JUnit', 'release', 'SysML', 'PHP', 'j2ee', 'EAR', 'Make', 'Eclipse',
                                         'license', 'webxml', 'SDK', 'EMF', 'applet', 'environment', 'platforms',
                                         'Agents', 'log4J', 'log4J2', 'workbench', 'Log', 'OS', 'Importxml', 'perl',
                                         'Mozilla', 'python', 'Bugzilla', 'OSX', 'Undeploy', 'javac', 'java', 'C++',
                                         'incompatible', 'compatibility', 'license', 'location', 'import', 'Facet',
                                         'JEE5', 'source', 'link', 'JFace', 'RDF', 'Navigator', 'upgrading',
                                         'incompatibility', 'Firefox'],
                 'network-issue': ['server', 'network', 'slow', 'exchange', 'http', 'ssh', 'HTTP',
                                   'shutdown', 'communication', 'protocol', 'ssl', 'traffic', 'url',
                                   'HttpClient', 'IP', 'ip', 'redirects', 'connection', 'sent', 'flushing',
                                   'connector', 'SocketException', 'connecting', 'entries', 'Socket',
                                   'addressess', 'Thunderbird', 'URI', 'URL', 'SSH', 'IPv6', 'IPv4'],
                 'database-issue': ['database', 'Database', 'pool', 'sql', 'connection', 'query', 'Encoding',
                                    'preference', 'Data', 'dialog', 'DBM', 'SQL'],
                 'gui-issue': ['page', 'render', 'select', 'view', 'font', 'image',
                               'layout', 'color', 'button', 'style', 'UI', 'screen', 'Alignment',
                               'backgroud-color', 'colour', 'background', 'elements', 'width', 'cell',
                               'table', 'space', 'visible', 'border', 'editing', 'area', 'Preferences',
                               'widget', 'icon', 'viewer', 'Widgets', 'SWT', 'BoxLayout', 'TabbedPane',
                               'Editor', 'kicking', 'refresh', 'wiped', 'GUI', 'Templatise', 'checkboxes',
                               'GIF', 'JPEG', 'PNG', 'scroll', 'horizontal', 'css', 'pixels', 'top', 'size',
                               'Text', 'Sidebar', 'JavaScript', 'box', 'layout', 'margins', 'image'],
                 'performance-issue': ['thread', 'infinite', 'loop', 'memory', 'leak', 'performance',
                                       'energy', 'leak', 'load', 'sleep', 'time', 'concurrent', 'OutOfMemoryError',
                                       'OutOfMemory', 'slowed', 'degradation', 'exceeding', 'Deadlock', 'deadlock',
                                       'repeats', 'requests', 'multiple', 'reloads'],
                 'permission-issue': ['violation', 'deprecated', 'goal', 'api', 'call', 'authentication', 'login',
                                      'permissions', 'permission', 'obsolete', 'Outdated', 'Migrate', '@Deprecated',
                                      'allocation'],
                 'security-issue': ['security', 'access', 'vulnerability', 'buffer', 'parameter', 'SecurityManager',
                                    'overflow', 'divide', 'zero', 'safe', 'encryption', 'DSA', 'key', 'packageaccess',
                                    'package-access', 'insecure', 'id', 'protections', 'secure'],
                 'functional-issue': ['error', 'crash', 'exception', 'return', 'alert', 'find', 'aborts'
                                      'terminate', 'null', 'pointer', 'bound', 'free', 'debug', 'code',
                                      'match', 'list', 'throws', 'NullPointerException', 'control', 'message',
                                      'ClassCastException', 'StringIndexOutOfBoundsException', 'Exception',
                                      'IndexOutOfBoundsException', 'IllegalArgumentException', 'fails',
                                      'broken', 'fails', 'erroneous', 'Corruption', 'Problem', 'condition',
                                      'cannot', 'doesn\'t', 'not', 'correct', 'fail', 'warnings', 'warning',
                                      'wrong', 'identifier', "don\'t", 'NPE'],
                 'test-issue': ['fail', 'test', 'retry', 'case', 'mock', 'run', 'testcases', 'suite',
                                'tests', 'testsuites', 'Regression', 'JUnit', 'mutation']}
    for type_key, type_value in type_dict.items():
        print type_key
        print [word_stemmer(i) for i in type_value]
        type_dict[type_key] = [word_stemmer(i) for i in type_value]
    with open('type/type.json', 'w') as f:
        json.dump(type_dict, f, indent=4)
    pass


if __name__ == '__main__':
    type_lib_build()
    print ''