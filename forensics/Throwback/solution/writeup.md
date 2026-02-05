# Throwback

If you open the hex of the `bin_weevils.jpg` (I also think some `file` and similar tools e.g. `exiftool` will detect this) you can notice a zip at the bottom of the JPG.

A `jpg` has a very specific ending byte: `0xFFD9` so everything after that is bonus.

To extract the hidden zip, use `binwalk -e bin_weevils.jpg`. Inside this zip, there is another image. Repeat.

Flag is in the final image.

---

Peter Walker