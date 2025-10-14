$(function () {
  /**
     * Reusable helper function to process the server's JSON response for an upload.
     * This is used by both the direct file uploader and the URL uploader.
     * @param {jQuery} itemElement - The jQuery object for the list item (<li>).
     * @param {object} response - The parsed JSON response from the server.
     */
  function handleUploadResponse(itemElement, response) {
    const rightPanel = $('.right', itemElement);
    itemElement.removeClass('upload-uploading');

    if (response.success) {
      if (response.duplicate) {
        itemElement.addClass('upload-duplicate');
        // Replace the panel's content with the duplicate confirmation HTML.
        rightPanel.html(response.confirm_duplicate_upload);
        // Event handlers for the confirmation are already delegated and will work.
      } else {
        itemElement.addClass('upload-success');
        // Replace the panel's content with the edit form HTML.
        rightPanel.html(response.form);
      }
    } else {
      itemElement.addClass('upload-failure');
      // Find the specific error message paragraph and set its text.
      rightPanel.find('.error_messages').text(response.error_message || 'Unknown error');
    }
  }

  /**
   * Reusable helper function to handle server/network errors during an upload.
   * @param {jQuery} itemElement - The jQuery object for the list item (<li>).
   * @param {object} xhr - The jQuery XHR object from the failed request.
   */
  function handleServerError(itemElement, xhr) {
    itemElement.removeClass('upload-uploading').addClass('upload-server-error');
    const errorMessage = $('.server-error', itemElement);
    $('.error-text', errorMessage).text(xhr.statusText);
    $('.error-code', errorMessage).text(xhr.status);
  }




  // 3. NEW: UPLOAD FROM URLS LOGIC
  $('#fetch-urls-button').on('click', function (e) {
    e.preventDefault();
    const $button = $(this);
    const uploadUrl = $button.data('url');
    const $collectionInput = $('select[name="collection"]');
    const urls = $('#url-input-area').val().split('\n').filter(url => url.trim() !== '');

    if (urls.length === 0) return;

    $button.prop('disabled', true);
    const requests = [];

    urls.forEach((url) => {
      const li = $($('#upload-list-item').html()).addClass('upload-uploading');
      li.find('.left').append(document.createTextNode(url));
      $('#upload-list').append(li);

      const postData = {
        'url': url,
        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
      };
      if ($collectionInput.length > 0) {
        postData.collection = $collectionInput.val();
      }

      const request = $.ajax({
        url: uploadUrl,
        type: 'POST',
        data: postData,
        dataType: 'json',
        success: (response) => {
          // REFACTORED: Use the helper function
          handleUploadResponse(li, response);
        },
        error: (xhr) => {
          // REFACTORED: Use the helper function
          handleServerError(li, xhr);
        },
        complete: () => {
          li.addClass('upload-complete');
        }
      });
      requests.push(request);
    });

    // When all URL fetch requests are done, re-enable the button
    $.when.apply($, requests).always(() => {
      $button.prop('disabled', false);
    });

    $('#url-input-area').val('');
  });
});
