import api from "../../api";

export const fetchCardsByDeckId = async ({ deck_id, to_study = true, query }) => {
  try {
    const { data } = await api.get("/cards", {
      params: { deck_id, to_study, query },
    });
    return data;
  } catch (error) {
    console.error("Error during getting cards:", error);
    return [];
  }
};

export const updateCardById = async ({ card_id, face = null, turnover = null, last_memorization_level = null }) => {
  try {
    const response = await api.patch(`/cards/${card_id}`, { face, turnover, last_memorization_level });
    return response.data;
  } catch (error) {
    console.error("Error during updating the card:", error);
    throw error;
  }
};

export const deleteCardById = async ({ card_id }) => {
  try {
    await api.delete(`/cards/${card_id}`)
  } catch (error) {
    console.error("Failed to delete a deck: ", error)
  }
};

export const createCard = async ({ face, turnover, deck_id }) => {
  try {
    const response = await api.post('/cards', { face, turnover, deck_id })
    return response.data;
  } catch (error) {
    console.log("Failed to create a deck: ", error)
  }
};
