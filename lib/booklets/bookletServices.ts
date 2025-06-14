// all services that deal with booklets, textblocks go here, services can access DB models
import { db } from '../db/drizzle';
import { booklets, rawMarkdownContent } from '../db/schema';
import { eq } from 'drizzle-orm';

interface BookletCreateRequest {
  title: string;
  rawMarkdownContent: string;
}

// stores the post processed BookletModel
interface BookletModel {}

// stores the post proceseds BookletTextBlockModel
interface BookletTextBlockModel {}

export async function createRawMarkdownContent(
  markdownContent: string
) {
  const newItem = {
    userId: 1,
    markdown: markdownContent,
    createdAt: new Date(),
    updatedAt: new Date(),
  };
  console.log('new item to insert ?? ', newItem)

  try {
    const [insertedItem] = await db
      .insert(rawMarkdownContent)
      .values(newItem)
      .returning();

    return insertedItem;
  } catch (error) {
    console.error('error inserting into rawMarkdownContent table', error);
    return null;
  }
}

export async function fetchRawMarkdownContent(id: number) {
  const item = await db
    .select()
    .from(rawMarkdownContent)
    .where(eq(rawMarkdownContent.id, id))
    .limit(1);
  return item;
}

export function createBooklet(bookletCreateReq: BookletCreateRequest) {
  return 'needs to be implement';
}

async function createBookletDatabase(title: string, userId: number) {
  const newBooklet = {
    userId,
    title,
    metadata_json: '{}',
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  const [insertedItem] = await db
    .insert(booklets)
    .values(newBooklet)
    .returning();

  return insertedItem;
}
