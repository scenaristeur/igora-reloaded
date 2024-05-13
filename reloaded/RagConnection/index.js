export class RagConnection {
    constructor(options = {}) {
        this.options = options
    }


    add(data){
        console.log("add", data)
    }

    search(data){
        console.log("search", data)
    }

}