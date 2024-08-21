ElevatedButton(
  onPressed: () {
    if (_image != null) {
      _uploadImage(_image!);
    }
  },
  child: Text('Analisar Imagem'),
),
