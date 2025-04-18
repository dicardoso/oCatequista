// the axios instance and types
import http from "../api";
import type { APIResponse } from "../types";
import type { Question, Answer } from "./types";

async function postQuestion(input: Question) {
  console.log("input", input);  
  return await http.post<APIResponse<Answer>>("perguntar", input);
}

export default {
    postQuestion
};