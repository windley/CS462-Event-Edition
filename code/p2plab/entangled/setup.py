#!/usr/bin/env python
#
# This file is part of Entangled, and is free software, distributed under the
# terms of the GNU Lesser General Public License Version 3, or any later
# version.
# See the COPYING file included in this archive

import os, sys

if sys.version_info < (2,5):
    print >>sys.stderr, "Entangled requires at least Python 2.5"
    sys.exit(3)
else:
    try:
        # Since Twisted does not provide egg-info by default, check if we can
        # import it instead of using install_requires in setup()
        import twisted
    except ImportError:
        print >>sys.stderr, "Entangled requires Twisted (Core) to be installed"
        sys.exit(3)

from setuptools import setup, find_packages, Command

class BuildAPIDocs(Command):
    """ setuptools Command to build documentation using epydoc """
    description = "build html API documentation"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import epydoc.cli
        except ImportError:
             print >>sys.stderr, "Epydoc (http://epydoc.sf.net) needs to be installed to build API documentation"
             sys.exit(3)
        else:
            print 'Building Entangled API documentation...'
            from epydoc.docbuilder import build_doc_index
            from epydoc.docwriter.html import HTMLWriter
            outputDir = '%s/doc/html' % os.path.abspath(os.path.dirname(__file__))
            docindex = build_doc_index(['entangled']) 
            htmlWriter = HTMLWriter(docindex, prj_name='Entangled',
                                    prj_url='http://entangled.sourceforge.net',
                                    inheritance='grouped', include_source_code=True)
            htmlWriter.write(outputDir)
            print 'API documentation created in: %s' % outputDir

setup(
      name='entangled',
      version='0.1',
      url='http://entangled.sourceforge.net',
      # Temporary download URL enabling SVN checkouts (until first file release)
      download_url='https://entangled.svn.sourceforge.net/svnroot/entangled#egg=entangled-0.1',
      
      packages=find_packages(),
      test_suite='tests/runalltests',

      author='Francois Aucamp',
      author_email='faucamp@csir.co.za',
      description='DHT based on Kademlia, and p2p tuple space implementation',
      license='LGPLv3+',
      keywords="dht distributed hash table kademlia peer p2p tuple space twisted",
      
      long_description='Entangled is a distributed hash table (DHT) based on '
                       'Kademlia, as well as a distributed, peer-to-peer '
                       'tuple space implementation. This can be used as a '
                       'base for creating peer-to-peer (P2P) network '
                       'applications that require synchronization and event '
                       'handling (such as distributed resource provisioning '
                       'systems) as well as applications that do not (such as '
                       'file sharing applications).',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Communications :: File Sharing',
          'Topic :: Internet',
          'Topic :: Software Development :: Libraries',
          'Topic :: System :: Networking',
          ],
      cmdclass={'build_apidocs': BuildAPIDocs}
)
