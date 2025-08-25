document.addEventListener("DOMContentLoaded", function () {
  const counters = document.querySelectorAll(".counter");
  const speed = 200; // semakin kecil semakin cepat

  counters.forEach(counter => {
    const animate = () => {
      const target = +counter.getAttribute("data-target");
      const count = +counter.innerText;

      // nilai tambah tiap langkah
      const increment = Math.ceil(target / speed);

      if (count < target) {
        counter.innerText = count + increment;
        setTimeout(animate, 20);
      } else {
        counter.innerText = target; // biar pas di angka akhir
      }
    };

    animate();
  });
});
