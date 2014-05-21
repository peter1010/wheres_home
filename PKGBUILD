pkgbase=track_my_ip
pkgname=('track_my_ip')
pkgver=2.7
pkgrel=4
pkgdesc="track_my_ip"
arch=('any')
url="http://pyserial.sf.net"
license=('custom:PYTHON')
makedepends=('python')
depends=('python')
source=()
md5sums=('794506184df83ef2290de0d18803dd11')
install='track_my_ip.install'

build() {
    ls
}

package() {
  cd ..
  python setup.py install --root=$pkgdir
}

