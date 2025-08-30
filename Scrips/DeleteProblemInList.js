// Hàm chờ element xuất hiện với MutationObserver (hiệu quả hơn polling)
function waitForElement(selector, textMatch, timeout = 3000) {
  return new Promise((resolve, reject) => {
    // Kiểm tra ngay lập tức xem element đã có chưa
    const existingEl = [...document.querySelectorAll(selector)].find(
        e => e.innerText?.trim() === textMatch);

    if (existingEl) {
      resolve(existingEl);
      return;
    }

    let timeoutId;
    const observer = new MutationObserver(() => {
      const el = [...document.querySelectorAll(selector)].find(
          e => e.innerText?.trim() === textMatch);

      if (el) {
        observer.disconnect();
        clearTimeout(timeoutId);
        resolve(el);
      }
    });

    // Quan sát thay đổi trong DOM
    observer.observe(document.body, {childList: true, subtree: true});

    // Timeout fallback
    timeoutId = setTimeout(() => {
      observer.disconnect();
      reject(new Error(
          `Timeout: Không tìm thấy element "${textMatch}" sau ${timeout}ms`));
    }, timeout);
  });
}

// Hàm delay với AbortController để có thể hủy
function delay(ms, signal) {
  return new Promise((resolve, reject) => {
    if (signal?.aborted) {
      reject(new Error('Aborted'));
      return;
    }

    const timeoutId = setTimeout(resolve, ms);

    signal?.addEventListener('abort', () => {
      clearTimeout(timeoutId);
      reject(new Error('Aborted'));
    });
  });
}

// Hàm tìm nút ellipsis với cách tìm linh hoạt hơn
function findEllipsisButton() {
  // Tìm theo data-icon trước
  let btn = document.querySelector('svg[data-icon="ellipsis"]')
                ?.closest('button,div,[role=\'button\']');

  // Nếu không có, tìm theo class hoặc các selector khác
  if (!btn) {
    btn =
        document
            .querySelector(
                '[data-testid*="ellipsis"], [aria-label*="more"], [aria-label*="options"]')
            ?.closest('button,div,[role=\'button\']');
  }

  return btn;
}

async function autoRemoveAll(options = {}) {
  const {
    maxRetries = 3,
    delayBetweenActions = 500,
    maxItems = Infinity,
    onProgress = null
  } = options;

  let removedCount = 0;
  let consecutiveErrors = 0;
  const abortController = new AbortController();

  console.log('🚀 Bắt đầu xóa bài...');

  // Thêm listener để có thể dừng bằng Ctrl+C trong console
  const stopHandler = (e) => {
    if (e.key === 'Escape' || (e.ctrlKey && e.key === 'c')) {
      console.log('⏹️ Đang dừng...');
      abortController.abort();
    }
  };
  document.addEventListener('keydown', stopHandler);

  try {
    while (removedCount < maxItems && !abortController.signal.aborted) {
      // Tìm nút ellipsis
      const ellipsisBtn = findEllipsisButton();

      if (!ellipsisBtn) {
        console.log('✅ Đã xóa hết bài! Tổng cộng:', removedCount);
        break;
      }

      let success = false;

      // Thử lại nếu thất bại
      for (let retry = 0; retry < maxRetries && !success; retry++) {
        try {
          if (retry > 0) {
            console.log(`🔄 Thử lại lần ${retry + 1}...`);
            await delay(
                delayBetweenActions * (retry + 1), abortController.signal);
          }

          // Click vào nút ellipsis
          ellipsisBtn.click();

          // Chờ menu xuất hiện và tìm nút Remove
          const removeBtn = await waitForElement(
              'li,div,span,button,[role=\'menuitem\']', 'Remove from List',
              2000);

          removeBtn.click();
          removedCount++;
          consecutiveErrors = 0;
          success = true;

          console.log(`🗑️ Đã xóa bài #${removedCount}`);

          // Callback progress nếu có
          onProgress?.(removedCount);

          // Chờ một chút để server xử lý
          await delay(delayBetweenActions, abortController.signal);

        } catch (error) {
          consecutiveErrors++;
          console.warn(`⚠️ Lỗi lần thử ${retry + 1}:`, error.message);

          // Nếu có menu đang mở, click ra ngoài để đóng
          document.body.click();
          await delay(300, abortController.signal);
        }
      }

      // Nếu thất bại quá nhiều lần liên tiếp, dừng lại
      if (!success) {
        consecutiveErrors++;
        if (consecutiveErrors >= 5) {
          console.error('❌ Quá nhiều lỗi liên tiếp. Dừng script.');
          break;
        }
      }
    }
  } catch (error) {
    if (error.message === 'Aborted') {
      console.log('⏹️ Script đã bị dừng.');
    } else {
      console.error('❌ Lỗi không mong muốn:', error);
    }
  } finally {
    document.removeEventListener('keydown', stopHandler);
    console.log(`📊 Kết thúc. Đã xóa ${removedCount} bài.`);
  }

  return removedCount;
}

// Cách sử dụng cơ bản
autoRemoveAll();

// Hoặc với tùy chọn nâng cao
/*
autoRemoveAll({
  maxRetries: 5,           // Thử lại tối đa 5 lần khi lỗi
  delayBetweenActions: 300, // Delay 300ms giữa các thao tác
  maxItems: 100,           // Chỉ xóa tối đa 100 bài
  onProgress: (count) => {  // Callback khi có progress
    if (count % 10 === 0) {
      console.log(`🎯 Milestone: Đã xóa ${count} bài`);
    }
  }
});
*/