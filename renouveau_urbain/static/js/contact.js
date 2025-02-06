document.addEventListener('DOMContentLoaded', () => {
      const form = document.getElementById('contact_form')
      const inputs = form.querySelectorAll('input, textarea')

      form.addEventListener('submit', event => {
            inputs.forEach(input => {
                  if (!input.checkValidity()) {
                        event.preventDefault()
                        event.stopPropagation()

                        validateField(input)
                  }
            }
            )
      })

      inputs.forEach(input => {
            input.addEventListener('input', () => {
                  validateField(input)
            })

            input.addEventListener('blur', () => {
                  validateField(input)
            })
      })


      function validateField(field) {
            let feedback = field.nextElementSibling

            if (feedback && field.validity.valid) {
                  field.classList.remove("is-invalid")
                  field.classList.add("is-valid")
                  feedback.textContent = ''
            }
            else {
                  field.classList.remove("is-valid")
                  field.classList.add("is-invalid")

                  if (field.validity.valueMissing) {
                        feedback.textContent = `${field.name.charAt(0).toUpperCase() + field.name.slice(1)} est requis !`
                  } else if (field.validity.tooShort) {
                        feedback.textContent = `${field.name.charAt(0).toUpperCase() + field.name.slice(1)} doit contenir au moins ${field.minLength} caractères !`
                  } else if (field.validity.tooLong) {
                        feedback.textContent = `${field.name.charAt(0).toUpperCase() + field.name.slice(1)} ne doit pas dépasser ${field.maxLength} caractères !`
                  } else if (field.validity.patternMismatch) {
                        feedback.textContent = `Le format du champ ${field.name} est incorrect !`;
                  }
                  else {
                        feedback.textContent = `Le champ ${field.name} est invalide !`;
                  }

            }


      }
})