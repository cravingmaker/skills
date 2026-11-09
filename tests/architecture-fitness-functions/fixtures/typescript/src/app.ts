import { read } from "./packages/a/index";
import { client } from "./packages/a/client";
import { calculate } from "./packages/b/index";
export const result = [read(), client, calculate()];
