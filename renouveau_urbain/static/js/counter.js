document.addEventListener("DOMContentLoaded", function () {
      const counters = document.querySelectorAll("[data-count]");
      
      const animateCounters = () => {
          counters.forEach(counter => {
              let target = +counter.getAttribute("data-count");
              let count = 0;
              let increment = target / 100;
  
              let updateCount = () => {
                  count += increment;
                  if (count < target) {
                      counter.innerText = Math.ceil(count);
                      requestAnimationFrame(updateCount);
                  } else {
                      counter.innerText = target;
                  }
              };
              updateCount();
          });
      };
  
      // Déclenchement au scroll
      let observer = new IntersectionObserver(entries => {
          entries.forEach(entry => {
              if (entry.isIntersecting) {
                  animateCounters();
              }
          });
      }, { threshold: 0.6 });
  
      observer.observe(document.querySelector("#stats"));
  });