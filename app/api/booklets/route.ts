import { NextRequest, NextResponse } from "next/server";
import { z } from "zod";
import { marked } from "marked";
import { createRawMarkdownContent } from "@/lib/booklets/bookletServices";

const CreateBookletRequest = z.object({
  title: z.string().nonempty(),
  rawMarkdownContent: z.string().nonempty(),
});

export async function POST(request: NextRequest) {
  try {
    const bookletCreateReq = CreateBookletRequest.parse(await request.json());

    if (
      await validateValidMarkdownString(bookletCreateReq.rawMarkdownContent) === null
    ) {
      return NextResponse.json(
        { error: "invalid markdown content" },
        { status: 400 }
      );
    }
    // 1) save the raw markdown in our database and 2) figure out how to parse an intemediate AST state from a valid markdown string
    console.info("continue processing Booklet...");
    const results = await createRawMarkdownContent(bookletCreateReq.rawMarkdownContent)
    console.info("createRawMarkdownContent results:", results);
    // Creating Booklets is a long process - can involve multiple LLM http calls and even
    // audio processing with voice llm models, we need to find a background process to handle
    // this work and return with work-id to the current http request

    const jobId = "success-job-id";
    return NextResponse.json({ jobId });
  } catch (error) {
    return NextResponse.json(
      { error: "failed to process the request" },
      { status: 500 }
    );
  }
}

// TODO research how to create background processes in Next?

async function validateValidMarkdownString(md: string): Promise<string | null> {
  try {
    const parsed = await marked.parse(md);
    console.info("markdown parsed:\n", parsed);
    return parsed;
  } catch (err) {
    console.error("invalid markdown content", err);
    return null;
  }
}
