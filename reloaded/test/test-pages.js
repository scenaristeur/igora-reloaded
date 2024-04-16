import * as chai from "chai";
import { expect } from "chai";
import chaiHttp from "chai-http";
chai.use(chaiHttp);

describe("Igora Reloaded API", () => {
  describe("GET /", () => {

    
    it("page d'accueil", (done) => {
      fetch("http://localhost:5678")
        .then((res) => {
           return res.text();
        })
        .then((res) => {
            expect(res).to.equal('Hello World');
            done()
        });
    }); 






  });
});
