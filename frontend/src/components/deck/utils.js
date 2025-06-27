import api from "../../api";

export const fetchDecks = async ({
  limit = 10,
  offset = 0,
  to_study = false,
  query,
} = {}) => {
  const params = {
    limit,
    offset,
    to_study,
    ...(query && { query }),
  };

  try {
    const { data } = await api.get("/decks", { params });
    return data;
  } catch (error) {
    console.error("Failed to fetch decks:", error);
    throw error;
  }
};

export const fetchDeckById = async ({ deck_id }) => {
  const { data } = await api.get(`/decks/${deck_id}`);
  return data;
};

export const createDeck = async ({ name }) => {
  const response = await api.post('/decks', { name });
  return response.data;
};

export const deleteDeck = async ({ deck_id }) => {
  await api.delete(`/decks/${deck_id}`)
}
