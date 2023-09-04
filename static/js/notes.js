const toggleLabelButton = document.getElementById('toggleLabelButton');
        const labelInput = document.getElementById('labelInput');
        const labelForm = document.getElementById('labelForm');
        let isAddingLabel = false;
        const toggleNoteButton = document.getElementById('toggleNoteButton');

        function openNoteForm(noteId, noteTitle, noteContent, addedLabels) {
            document.getElementById("noteTitle").value = noteTitle;
            document.getElementById("noteContent").value = noteContent;

            document.getElementById("noteFormButton").style.display = noteTitle ? "none" : "block";

            const multiLabelsSelect = document.getElementById("multiLabels");
            for (let i = 0; i < multiLabelsSelect.options.length; i++) {
                const option = multiLabelsSelect.options[i];
                if (addedLabels.includes(option.textContent)) {
                    option.selected = true;
                } else {
                    option.selected = false;
                }
            }

            if (typeof $(multiLabelsSelect).selectpicker === 'function') {
                $(multiLabelsSelect).selectpicker('refresh');
            }

            document.getElementById('noteForm').style.display = 'block'
            document.getElementById('overlay').style.display = 'block'
        }
    
        toggleLabelButton.addEventListener('click', () => {
            if (isAddingLabel) {
                labelForm.submit();
            } else {
                labelInput.style.display = 'flex';
                toggleLabelButton.value = 'Add Label';
                isAddingLabel = true;
            }
        });

        document.querySelector('.overlay').addEventListener('click', () => {
            document.getElementById("noteForm").style.display = 'none';
            document.querySelector('.overlay').style.display = 'none';
        });
        
        toggleNoteButton.addEventListener('click', () => {
            openNoteForm("", "", "", "");
            document.getElementById("noteForm").style.display = 'block';
            document.querySelector('.overlay').style.display = 'block';
        });

        const noteElements = document.querySelectorAll('.note');
        noteElements.forEach((noteElement) => {
            noteElement.addEventListener('click', () => {
                if (event.target.classList.contains('fas')) {
                    return;
                }
                const noteId = noteElement.id;
                const noteTitle = noteElement.querySelector('.note-title').textContent;
                const noteContent = noteElement.querySelector('p.note-content').textContent; 

                const labels = noteElement.querySelectorAll('.note-label');
                const addedLabels = [];
                labels.forEach((noteLabel) => {
                    console.log(noteLabel.textContent);
                    addedLabels.push(noteLabel.textContent);
                });

                openNoteForm(noteId, noteTitle, noteContent, addedLabels);
            });
        });
    
        labelForm.addEventListener('submit', (event) => {
            if (!isAddingLabel) {
                event.preventDefault();
            }
        });