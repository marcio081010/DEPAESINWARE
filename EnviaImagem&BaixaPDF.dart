import 'package:dio/dio.dart';
import 'package:path_provider/path_provider.dart';
import 'package:open_file/open_file.dart';

Future<void> _uploadImage(File image) async {
  final dio = Dio();

  try {
    FormData formData = FormData.fromMap({
      'file': await MultipartFile.fromFile(image.path),
    });

    final response = await dio.post(
      'http://seu-backend-url.com/detect',  // Substitua pela URL da sua API
      data: formData,
    );

    if (response.statusCode == 200) {
      final directory = await getApplicationDocumentsDirectory();
      final file = File('${directory.path}/relatorio_patologia.pdf');
      file.writeAsBytes(response.data);
      OpenFile.open(file.path);
    }
  } catch (e) {
    print('Erro ao enviar a imagem: $e');
  }
}
