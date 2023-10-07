let carouselIndex = 0;
let comicRow = null;

// Function to update the status on the page
function updateStatus(message) {
  const statusText = document.getElementById('status-text');
  const spinner = document.getElementById('spinner');
  if (message) {
    spinner.style.display = 'block';
  } else {
    spinner.style.display = 'none';
  }
  statusText.innerHTML = message;
}

document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById("imageModal");
    const modalImg = document.getElementById("modalImage");
    const span = document.getElementsByClassName("close")[0];  
    const generateComicButton = document.getElementById('generateComicButton');
    const comicDiv = document.getElementById('comicContainer');  
              
    // Add an event listener to each image in the 'examples'
    document.getElementById('examples').addEventListener("click", function(event) {
      if (event.target.tagName === "IMG") {
        modal.style.display = "flex";
        modalImg.src = event.target.src;
      }
    });  

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
      modal.style.display = "none";
    }

    async function displaySingleComicPanel(panel_text, index) {
      // Fetch panel data from the Flask backend
      const response = await fetch('/generate_single_comic_panel', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ panel_text }),
      });

      const panelData = await response.json();
      const panel = panelData.comic_panel;

      // Create new comic panel using your HTML/CSS structure
      const comicPanel = document.createElement('div');
      comicPanel.className = 'panel';

      // Set narration text
      const narrationText = document.createElement('p');
      narrationText.className = 'text top-left'; 
      narrationText.innerText = panel.narration;

      // Set image
      const panelImage = document.createElement('img');
      panelImage.src = panel.image_url;  // Assuming your API response includes this
      panelImage.alt = "Comic panel image";
      panelImage.className = "comic-image";

      comicPanel.appendChild(narrationText);
      comicPanel.appendChild(panelImage);

      // Append the new panel to the existing comic row
      if (index % 2 === 0) {
        comicRow = document.createElement('div');
        comicRow.className = 'comic-row';
      }

      comicRow.appendChild(comicPanel);

      if (index % 2 === 1 || index === panelData.length - 1) {
        comicDiv.appendChild(comicRow);
      }
    }
  
    generateComicButton.addEventListener('click', async () => {
      try {
        // Coletar sinopse do usuário
        const synopsis = document.getElementById("synopsis").value;

        // Validar o campo de sinopse
        if (!synopsis) {
          alert('Por favor, forneça uma sinopse.');
          updateStatus('');
          return;
        }

        // Ativar o spinner
        updateStatus('Gerando gibi com IA. Isso pode demorar alguns minutos...');

        // Buscar painéis de quadrinhos do servidor
        const response = await fetch('/generate_comic_output', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ synopsis: synopsis }),
        });

        const comicData = await response.json();
        const comicOutputArray = comicData.comic_output;

        comicDiv.innerHTML = '';  // Clear existing panels

        for (let i = 0; i < comicOutputArray.length; i++) {
          updateStatus('Criando Gibi usando IA. Criando painel ' + (i + 1) + ' de ' + comicOutputArray.length + '...');
          await displaySingleComicPanel(comicOutputArray[i], i);
        }

        // Handle the last row if there is an odd number of panels
        if (comicOutputArray.length % 2 !== 0) {
          comicDiv.appendChild(comicRow);
        }

        updateStatus('');
      } catch (error) {
        comicDiv.innerHTML = '<p>Error: ' + error + '</p>';
        updateStatus('');
      }
    });
    
    document.getElementById('prevBtn').addEventListener('click', () => {
      move(-2);  // Move two items back
    });

    document.getElementById('nextBtn').addEventListener('click', () => {
      move(2);  // Move two items forward
    });

    function move(step) {
      const wrapper = document.querySelector('.carousel-wrapper');
      carouselIndex += step;
      carouselIndex = Math.max(0, Math.min(carouselIndex, wrapper.children.length - 2));  // Adjust here to stop at the correct item
      const newOffset = -carouselIndex * 300;  // 300 is the width of each carousel item
      wrapper.style.transform = `translateX(${newOffset}px)`;
    }
  
});