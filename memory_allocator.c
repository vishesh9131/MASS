#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>

#define POOL_SIZE 1024 * 1024 * 10  // 10 MB pool size
#define ALIGNMENT 8  // 8-byte alignment

static char memory_pool[POOL_SIZE];
static size_t pool_offset = 0;
static pthread_mutex_t pool_mutex = PTHREAD_MUTEX_INITIALIZER;

void* allocate_memory(size_t size) {
    pthread_mutex_lock(&pool_mutex);

    // Align the size
    size_t aligned_size = (size + (ALIGNMENT - 1)) & ~(ALIGNMENT - 1);

    if (pool_offset + aligned_size > POOL_SIZE) {
        fprintf(stderr, "Memory pool exhausted\n");
        pthread_mutex_unlock(&pool_mutex);
        return NULL;
    }

    void* ptr = memory_pool + pool_offset;
    pool_offset += aligned_size;

    fprintf(stdout, "Allocated %zu bytes at %p\n", aligned_size, ptr);

    pthread_mutex_unlock(&pool_mutex);
    return ptr;
}

void* reallocate_memory(void* ptr, size_t new_size) {
    pthread_mutex_lock(&pool_mutex);

    if (ptr == NULL) {
        pthread_mutex_unlock(&pool_mutex);
        return allocate_memory(new_size);
    }

    // Align the new size
    size_t aligned_new_size = (new_size + (ALIGNMENT - 1)) & ~(ALIGNMENT - 1);

    if (pool_offset + aligned_new_size > POOL_SIZE) {
        fprintf(stderr, "Memory pool exhausted\n");
        pthread_mutex_unlock(&pool_mutex);
        return NULL;
    }

    void* new_ptr = memory_pool + pool_offset;
    pool_offset += aligned_new_size;

    // Copy the old data to the new location
    memcpy(new_ptr, ptr, aligned_new_size);

    fprintf(stdout, "Reallocated to %zu bytes at %p\n", aligned_new_size, new_ptr);

    pthread_mutex_unlock(&pool_mutex);
    return new_ptr;
}

void free_memory(void* ptr) {
    // In a simple memory pool, free is a no-op
    fprintf(stdout, "Freed memory at %p\n", ptr);
}

void reset_memory_pool() {
    pthread_mutex_lock(&pool_mutex);
    pool_offset = 0;
    fprintf(stdout, "Memory pool reset\n");
    pthread_mutex_unlock(&pool_mutex);
}