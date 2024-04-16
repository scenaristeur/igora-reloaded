import { v4 as uuidv4 } from "uuid";
export class ChatCompletionResponse {
  constructor(options = {}) {
    this.id = "chatcmpl-" + uuidv4();
    this.isStream(options);
    this.created = Math.floor(Date.now() / 1000);
    this.model = options.model;
    (this.system_fingerprint = "fp_" + uuidv4()),
      (this.usage = {
        prompt_tokens: 0,
        completion_tokens: 0,
        total_tokens: 0,
      });
  }

  isStream(options) {
    if (options.stream) {
      this.object = "chat.completion.chunk";
      this.choices = [
        {
          index: 0,
          delta: {
            role: "assistant",
            content: "",
          },
          logprobs: null,
          finish_reason: null,
        },
      ];
    } else {
      this.object = "chat.completion";
      this.choices = [
        {
          index: 0,
          message: {
            role: "assistant",
            content: "\n\nHello there, how may I assist you today?",
          },
          logprobs: null,
          finish_reason: "stop",
        },
      ];
    }
  }

  updateContent(content, chunkDate) {
    console.log("UPDATEcontent", content);
    this.choices[0].delta.content = content;
    this.chunkDate = chunkDate;
  }
  finish(reason) {
    this.choices[0].finish_reason = reason;
    // this.choices[0].delta.content = "{}" // Does not seems necessary for crewai
  }
  toString() {
    console.log("toString", JSON.stringify(this));
    return JSON.stringify(this);
  }
}
