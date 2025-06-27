function toggleCollectionDisplay() {
      const collectionDecks = document.querySelector('.collection-decks');
      const showCollectionsIcon = document.getElementById("showCollections");
      const hideCollectionsIcon = document.getElementById("hideCollections");

      const isHidden = collectionDecks.classList.toggle('hidden');

      if (isHidden) {
          showCollectionsIcon.style.display = 'inline';
          hideCollectionsIcon.style.display = 'none';
      } else {
          showCollectionsIcon.style.display = 'none';
          hideCollectionsIcon.style.display = 'inline';
      }
  }

  document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("hideCollections").style.display = "none";
});

export default toggleCollectionDisplay
