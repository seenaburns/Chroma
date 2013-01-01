from distutils.core import setup

setup(
    name='Chroma',
    version='0.1.3',
    author='Seena Burns',
    author_email='hello@seenaburns.com',
    url='https://github.com/seenaburns/Chroma',
    license=open('LICENSE.txt').read(),
    description='Color handling made simple.',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    packages=['chroma'],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ),
)
