const express = require('express');
const multer = require('multer');
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const cors = require('cors');

const app = express();

// Habilitar CORS
app.use(cors());

// Configuração do Multer
const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, 'uploads/')
    },
    filename: function (req, file, cb) {
        cb(null, Date.now() + '-' + file.originalname)
    }
});

// Criar diretório uploads se não existir
if (!fs.existsSync('uploads')){
    fs.mkdirSync('uploads');
}

const upload = multer({ storage: storage });

app.post('/upload', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'Nenhuma imagem enviada' });
        }

        const formData = new FormData();
        formData.append('image', fs.createReadStream(req.file.path));

        const response = await axios.post('http://localhost:5000/analyze-image', formData, {
            headers: {
                ...formData.getHeaders()
            }
        });

        // Limpar arquivo após uso
        fs.unlinkSync(req.file.path);

        res.json(response.data);
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ 
            error: 'Erro ao processar imagem',
            details: error.message 
        });
    }
});

app.post('/analyze-colors', upload.single('file'), async (req, res) => {
    try {
        if (!req.file) {
            return res.status(400).json({ error: 'Nenhuma imagem enviada' });
        }

        const formData = new FormData();
        formData.append('image', fs.createReadStream(req.file.path));

        const response = await axios.post('http://localhost:5000/analyze-colors', formData, {
            headers: {
                ...formData.getHeaders()
            }
        });

        // Limpar arquivo após uso
        fs.unlinkSync(req.file.path);

        res.json(response.data);
    } catch (error) {
        console.error('Erro:', error);
        res.status(500).json({ 
            error: 'Erro ao analisar cores',
            details: error.message 
        });
    }
});

// Adicionar rota para servir o arquivo HTML
app.use(express.static('.')); // Serve arquivos estáticos do diretório atual

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Servidor Node.js rodando na porta ${PORT}`);
});