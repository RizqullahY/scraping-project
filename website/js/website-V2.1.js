$(document).ready(function () {
    const wrapper = $(".wrapper");
    let index = 1;
    let consecutiveFails = 0;
    const maxFails = 5; 
  
    function loadNextImage() {
      const imgPath = `./image_${index}.jpg`;
      const img = new Image();
  
      img.onload = function () {
        const imgElement = $(`<img src="${imgPath}" alt="Image ${index} Sudah Habis Atau Sudah Error" />`);
        wrapper.append(imgElement);
        index++;
        consecutiveFails = 0; // reset karena sukses
        loadNextImage(); // lanjut
      };
  
      img.onerror = function () {
        console.log(`Gagal load: ${imgPath}`);
        consecutiveFails++;
        index++;
        if (consecutiveFails < maxFails) {
          loadNextImage(); // masih coba lagi
        } else {
          console.log("Selesai, gak nemu gambar lagi.");
        }
      };
  
      img.src = imgPath;
    }
  
    loadNextImage();
  });
  