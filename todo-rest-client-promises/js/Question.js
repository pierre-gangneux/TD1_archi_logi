class Question{
    // Les datas de la question
    constructor(data){
        this.id_questionnaire = data.id_questionnaire;
        this.id = data.id;
        this.title = data.title;
        this.type = data.type;
        console.log(data)
    }
}
