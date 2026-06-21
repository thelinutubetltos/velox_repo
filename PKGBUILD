pkgname=velox-wallpapers
pkgver=1.1
pkgrel=1
pkgdesc="Official Velox Linux wallpapers"
arch=('any')
url="https://github.com/thelinutubetltos/velox-iso"
license=('custom')
source=()

package() {
    local wall_src="$startdir/velox-wallpapers"
    local i src_file

    for i in $(seq 1 15); do
        mkdir -p "$pkgdir/usr/share/wallpapers/Velox-${i}/contents/images"
        src_file=$(ls "${wall_src}/velox wall ${i}.png" "${wall_src}/velox wall ${i} .png" 2>/dev/null | head -1)
        [[ -z "$src_file" ]] && { echo "WARNING: velox wall ${i}.png not found"; continue; }
        install -m644 "$src_file" "$pkgdir/usr/share/wallpapers/Velox-${i}/contents/images/3840x2160.png"
        cat > "$pkgdir/usr/share/wallpapers/Velox-${i}/metadata.json" << EOF
{
    "KPlugin": {
        "Authors": [{"Name": "Velox Linux"}],
        "Id": "Velox-${i}",
        "License": "CC-BY-SA-4.0",
        "Name": "Velox ${i}"
    }
}
EOF
    done
}
