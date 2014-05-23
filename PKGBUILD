pkgbase=track_my_ip
pkgname=('track_my_ip')
pkgver=1.0
pkgrel=1
pkgdesc="track_my_ip"
arch=('any')
url="http://pyserial.sf.net"
license=('custom:PYTHON')
makedepends=('python')
depends=('python' 'msmtp-mta')
source=()
#md5sums=('794506184df83ef2290de0d18803dd11')
install='track_my_ip.install'

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

