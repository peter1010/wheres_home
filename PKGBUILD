pkgbase=wheres_home
pkgname=('wheres_home')
pkgver=1.0
pkgrel=2
pkgdesc="wheres_home"
arch=('any')
url="github"
license=('GPL')
makedepends=('python')
depends=('python' 'msmtp-mta')
source=()
install='wheres_home.install'

pkgver() {
    python ../setup.py -V
}

check() {
    pushd ..
    python setup.py check
    popd
}

package() {
    pushd ..
    DONT_START=1 python setup.py install --root=$pkgdir
    popd
}

