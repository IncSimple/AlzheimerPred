import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "Alzheimer's Prediction",
      theme: ThemeData(primarySwatch: Colors.blue),
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _prediction = "No prediction yet";
  bool _isLoading = false;

  Future<void> _pickImageAndPredict() async {
    final picker = ImagePicker();
    final pickedFile = await picker.pickImage(source: ImageSource.gallery);

    if (pickedFile == null) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse("http://10.0.2.2:5000/predict"), // Change for a real device
      );

      request.files.add(
        await http.MultipartFile.fromPath("image", pickedFile.path),
      );

      var response = await request.send();

      if (response.statusCode == 200) {
        final result = jsonDecode(await response.stream.bytesToString());
        setState(() {
          _prediction = "Prediction: ${result['prediction']}";
        });
      } else {
        setState(() {
          _prediction = "Server Error: ${response.reasonPhrase}";
        });
      }
    } catch (e) {
      setState(() {
        _prediction = "Network Error: $e";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Alzheimer's Prediction")),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text(
              "Upload an image for Alzheimer's Prediction",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 20),
            _isLoading
                ? const CircularProgressIndicator()
                : ElevatedButton(
                  onPressed: _pickImageAndPredict,
                  child: const Text("Upload Image"),
                ),
            const SizedBox(height: 20),
            Text(
              _prediction,
              style: const TextStyle(fontSize: 16, color: Colors.black87),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
