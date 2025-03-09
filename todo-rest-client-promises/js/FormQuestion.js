class FormQuestion extends HTMLLIElement {
    // Le formulaire de la question
    constructor(formQuestionnaire){
        // Création de l'élément li
        super();
        this.style.margin = "1em";
        this.style.border = '0.1em solid black';
        this.style.width = "fit-content";
        this.style.listStyle = "none";
        this.style.borderRadius = "15px";
        formQuestionnaire.querySelector('#listeQuestions').append(this);
        this.formQuestionnaire = formQuestionnaire;

        // Création de l'élément du titre de la question
        let titre = document.createElement('div');
        this.append(titre);

        titre.style.display = "flex";
        titre.style.alignItems = "center"
        titre.style.justifyContent = "space-between"
        titre.style.padding = "0.3em";
        titre.style.gap = "0.5em";

        // Création du label du titre de la question
        let titreQuestion = document.createElement('label');
        titreQuestion.setAttribute('for', 'titreQuestion');
        titreQuestion.setAttribute('id', 'titreQuestionLabel');
        titreQuestion.textContent = 'Titre';
        titre.append(titreQuestion);

        // Création de l'input du titre de la question
        let titreQuestionInput = document.createElement('input');
        titreQuestionInput.id = 'titreQuestion';
        titre.append(titreQuestionInput);

        titreQuestionInput.style.padding = "0.5em";
        titreQuestionInput.style.borderRadius = "15px";
        titreQuestionInput.style.border = "none";

        // Création de l'élément du type de la question
        let type = document.createElement('div');
        this.append(type);

        type.style.display = "flex";
        type.style.alignItems = "center";
        type.style.justifyContent = "space-between";
        type.style.padding = "0.3em";
        type.style.gap = "0.5em";

        // Création du label du type de la question
        let typeQuestion = document.createElement('label');
        typeQuestion.setAttribute('for', 'typeQuestion');
        typeQuestion.setAttribute('id', 'typeQuestionLabel');
        typeQuestion.textContent = 'Type';
        type.append(typeQuestion);

        // Création du selecteur du type de la question
        let typeQuestionSelect = document.createElement('select');
        typeQuestionSelect.id = 'typeQuestion';
        let optionSelectQuestion1 = document.createElement('option');
        optionSelectQuestion1.value = "simple"
        optionSelectQuestion1.textContent = "simple"
        let optionSelectQuestion2 = document.createElement('option');
        optionSelectQuestion2.value = "multiple"
        optionSelectQuestion2.textContent = "multiple"
        typeQuestionSelect.appendChild(optionSelectQuestion1)
        typeQuestionSelect.appendChild(optionSelectQuestion2)
        type.append(typeQuestionSelect);

        typeQuestionSelect.style.padding = "0.5em";
        typeQuestionSelect.style.borderRadius = "15px";
        typeQuestionSelect.style.border = "none";

        // Boutons de gestion de la question
        let boutons = document.createElement('div');
        boutons.id = 'boutonsQuestion';
        this.append(boutons);

        // Création du bouton pour enregistrer la nouvelle question
        let saveQuestion = document.createElement('img');
        saveQuestion.src = 'img/save.png';
        
        saveQuestion.onclick = () => this.saveNewQuestion();
        boutons.append(saveQuestion);
    }

    fillFormQuestion(question){
        // Set de l'id et de la question
        this.question = question;

        // Set de la valeur du titre de la question
        let titreQuestionInput = this.querySelector('#titreQuestion');
        titreQuestionInput.value = question.title;
    
        // Set de la valeur du type de la question
        let typeQuestionSelect = this.querySelector('#typeQuestion');
        typeQuestionSelect.value = question.type;
    
        // Boutons de gestion de la question
        let boutons = this.querySelector('#boutonsQuestion');
        Utilitaire.clearContent(boutons);

        // Création du bouton pour supprimer la question
        let deleteQuestionButton = document.createElement('img');
        deleteQuestionButton.src = 'img/delete.png';
        deleteQuestionButton.onclick = () => this.deleteQuestion();
        boutons.append(deleteQuestionButton);

        // Création du bouton pour sauvegarder les modifications de la question
        let saveQuestion = document.createElement('img');
        saveQuestion.src = 'img/save.png';
        saveQuestion.onclick = () => this.saveModifiedQuestion();
        boutons.append(saveQuestion);
    }

    saveNewQuestion(){
        console.log("héoh")
        console.log(this)
        // Récupère la valeur du title de la question
        let title = this.querySelector('#titreQuestion').value;
        // Récupère la valeur du type de la question
        let type = this.querySelector('#typeQuestion').value;
        
        // Récupère les erreurs
        const errors = [];
        if (!title) errors.push("Il est impossible de créer une question avec un title vide");
        if (!type) errors.push("Il est impossible de créer une question avec un type vide");
        if (errors.length){
            // S'il y a des erreurs, les affiches
            errors.forEach(error => Utilitaire.errorClient(error));
        }
        // S'il n'y a pas d'erreurs
        else {
            // Création de la requête permettant de modifier la question
            
            fetch('http://localhost:5000/api/questionnaires/'+this.formQuestionnaire.questionnaire.id+'/questions',{
            headers: {'Content-Type': 'application/json'},
            method: 'POST',
            body: JSON.stringify({"title":title, "type":type, "questionnaire_id":this.formQuestionnaire.questionnaire.id})
            })
            .then(response => {
                if (response.ok){
                    Utilitaire.successMessage('Insert Success');
                    return response.json();
                }
                else throw new Error('Problème ajax: ' + response.status);
            })
            .then(async dataQuestion => {
                // On met à jour la liste des questions du questionnaire
                await this.formQuestionnaire.questionnaire.getQuestions();
                // On affiche la question nouvellement créer
                this.fillFormQuestion(this.formQuestionnaire.questionnaire.getQuestion(dataQuestion.id));
            })
            .catch(Utilitaire.errorServeur);
        }
    }
    
    saveModifiedQuestion(){
        // Récupère la valeur du title de la question
        let title = this.querySelector('#titreQuestion').value;
        // Récupère la valeur du type de la question
        let type = this.querySelector('#typeQuestion').value;
        let bodyRequest = {'question_id':this.question.id};

        // Regarde si le titre à changer et s'il n'est pas vide
        if (this.question.title != title){
            if (title != ''){
                bodyRequest.title = title;
            }
            else{
                Utilitaire.errorClient("Il n'est pas possible d'avoir un titre vide");
            }
        }
        // Regarde si le type à changer et s'il n'est pas vide
        if (this.question.type != type){
            if (type != ''){
                bodyRequest.type = type;
            }
            else{
                Utilitaire.errorClient("Il n'est pas possible d'avoir un type vide")
            }
        }
        // S'il y a une modification, on envoi une requête
        if (Object.keys(bodyRequest).length > 1){
            // Création de la requête permettant de modifier la question
            fetch('http://localhost:5000/api/questionnaires/'+this.formQuestionnaire.questionnaire.id+'/questions',{
                headers: {'Content-Type': 'application/json'},
                method: 'PUT',
                body: JSON.stringify(bodyRequest)
            })
            .then(response => {
                //if (response.ok){
                    Utilitaire.successMessage('Update Success');
                    return response.json();
                //}
                //else throw new Error('Problème ajax: ' + response.status);
            })
            .then(async dataQuestion => {
                // On met à jour la liste des questions du questionnaire
                await this.formQuestionnaire.questionnaire.getQuestions();
                // On affiche la question modifier
                this.fillFormQuestion(this.formQuestionnaire.questionnaire.getQuestion(dataQuestion.id));
            })
            .catch(Utilitaire.errorServeur);
        }
        // Sinon, on ne fait rien
        else{
            Utilitaire.errorClient("Aucun changement de fait");
        }
    }
    
    deleteQuestion(){
        // Création de la requête permettant de supprimer la question
        fetch('http://localhost:5000/api/questionnaires/'+this.formQuestionnaire.questionnaire.id+'/questions',{
            headers: {'Content-Type': 'application/json'},
            method: 'DELETE',
            body: JSON.stringify({"question_id":this.question.id})
        })
        .then(async response => {
            if (response.ok){
                Utilitaire.successMessage('Delete Success');
                // On met à jour la liste des questions du questionnaire
                await this.formQuestionnaire.questionnaire.getQuestions();
                return response.json();
            }
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(dataQuestion => {
            Utilitaire.successMessage(`Supression de la question ${dataQuestion.title}`);
            // On supprime le formulaire
            this.remove();
        })
        .catch(Utilitaire.errorServeur);
    }
}
customElements.define("form-question", FormQuestion, { extends: "li" });
