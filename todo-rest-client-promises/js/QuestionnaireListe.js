class QuestionnaireListe extends HTMLUListElement {
    constructor(){
        if (QuestionnaireListe.instance) {
            return QuestionnaireListe.instance;
        }
        super();
        QuestionnaireListe.instance = this;
        return this;
    }

    static getQuestionnaireListe(){
        // Si l'instance n'existe pas, on la créer et l'affiche
        if (!QuestionnaireListe.instance){
            QuestionnaireListe.instance = new QuestionnaireListe();
            document.getElementById('questionnaires').appendChild(QuestionnaireListe.instance);
        }
        return QuestionnaireListe.instance;
    }

    async remplirQuestionnaires(questionnaires){questionnaires.forEach(questionnaireData => this.appendChild(new Questionnaire(questionnaireData)))}

    async refreshQuestionnaireList(){
        Utilitaire.clearContent(this);
        await fetch('http://127.0.0.1:5000/api/questionnaires')
        .then(response => {
            if (response.ok) return response.json();
            else throw new Error('Problème ajax: ' + response.status);
        })
        .then(async questionnaires => await this.remplirQuestionnaires(questionnaires))
        .catch(err => Utilitaire.errorServeur(err, 'Impossible de récupérer les questionnaires à réaliser !'));
    }

    getQuestionnaire(questionnaireId){for(let questionnaire of this.children){if (parseInt(questionnaire.id) === questionnaireId){return questionnaire;}}}
}
customElements.define("questionnaire-liste", QuestionnaireListe, { extends: "ul" });
