<script setup>
import { onMounted, ref } from "vue";

const notes = ref([]);
const content = ref("");
const loading = ref(false);

async function loadNotes() {
  const res = await fetch("/api/notes");
  notes.value = await res.json();
}

async function addNote() {
  const c = content.value.trim();
  if (!c) return;

  loading.value = true;
  try {
    await fetch("/api/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: c }),
    });
    content.value = "";
    await loadNotes();
  } finally {
    loading.value = false;
  }
}

onMounted(loadNotes);
</script>

<template>
  <div style="max-width: 560px; margin: 40px auto; font-family: system-ui">
  <h1>Bài kiểm tra -MSSV- Ca2 </h1>
    <h2>Notes</h2>

    <div style="display: flex; gap: 8px">
      <input v-model="content" placeholder="Write a note..." style="flex: 1; padding: 10px" />
      <button :disabled="loading" @click="addNote" style="padding: 10px 14px">
        {{ loading ? "Adding..." : "Add" }}
      </button>
    </div>

    <ul style="margin-top: 16px">
      <li v-for="n in notes" :key="n.id">#{{ n.id }} - {{ n.content }}</li>
    </ul>
  </div>
</template>
