import { AntDesign } from "@expo/vector-icons";
import { LinearGradient } from 'expo-linear-gradient';
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import {
  Alert,
  Animated,
  Image,
  Keyboard,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
  useWindowDimensions
} from 'react-native';
import { useNavigation } from '@react-navigation/native';

const Cadastro = () => {
  const navigation = useNavigation();
  const { width } = useWindowDimensions();

  const clamp = useCallback((val, min, max) => Math.max(min, Math.min(max, val)), []);
  const rf = useCallback((size) => Math.round(clamp(size * (width / 390), 12, 30)), [width, clamp]);

  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [isPressing, setIsPressing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const fadeAnim = useRef(new Animated.Value(0)).current;
  const debounceRef = useRef(null);

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 600,
      useNativeDriver: true,
    }).start();
  }, [fadeAnim]);

  const validateFields = useCallback(() => {
    const newErrors = {};
    if (!nome.trim()) newErrors.nome = 'Informe um nome válido.';
    if (!email.includes('@')) newErrors.email = 'Email inválido.';
    if (senha.length < 6) newErrors.senha = 'A senha deve ter pelo menos 6 caracteres.';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [nome, email, senha]);

  const handleCadastro = useCallback(async () => {
    if (loading) return;

    if (!validateFields()) return;

    setLoading(true);
    clearTimeout(debounceRef.current);

    try {
      const response = await fetch('http://localhost:8000/api/users/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: Date.now(),
          email,
          username: nome.replace(/\s+/g, '').toLowerCase(),
          name: nome,
          password_hash: senha,
          latitude: 0.0,
          longitude: 0.0,
          type: 'normal',
          created_at: new Date().toISOString().split('T')[0],
        }),
      });

      if (response.ok) {
        const data = await response.json();
        Alert.alert('Cadastro', 'Usuário cadastrado com sucesso!');
        console.log('Usuário criado:', data);
      } else {
        const errorData = await response.json();
        Alert.alert('Erro', `Falha no cadastro: ${errorData.detail || 'Erro desconhecido'}`);
        console.error('Erro no cadastro:', errorData);
      }
    } catch (error) {
      Alert.alert('Erro', 'Erro de conexão com o servidor.');
      console.error('Erro de rede:', error);
    } finally {
      setLoading(false);
    }
  }, [nome, email, senha, loading, validateFields]);

  const dynamicStyles = useMemo(
    () => ({
      logoContainer: { marginTop: rf(-40), marginBottom: rf(20) },
      logo: { width: 200, height: 200 },
      formPadding: { paddingHorizontal: rf(25) },
      input: {
        width: '100%',
        minHeight: rf(70),
        height: rf(70),
        fontSize: rf(17),
        paddingHorizontal: rf(15),
        paddingVertical: rf(10),
        marginVertical: rf(8),
      },
      botao: { width: '100%', paddingVertical: rf(12), borderRadius: rf(40), marginTop: rf(20) },
      textoBotao: { fontSize: rf(19) },
      titulo: { fontSize: rf(26), marginBottom: rf(20) },
    }),
    [rf]
  );

  return (
    <Pressable onPress={Keyboard.dismiss} accessible={false}>
      <LinearGradient colors={['#8000d5', '#f910a3', '#fddf00']} style={styles.gradient}>
        <SafeAreaView style={styles.safe}>
          <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.flex}
          >
            <ScrollView
              contentContainerStyle={{
                flexGrow: 1,
                justifyContent: 'center',
                alignItems: 'center',
              }}
              keyboardShouldPersistTaps="handled"
            >
              <TouchableOpacity style={styles.backCircle} onPress={() => navigation.goBack()}>
                <AntDesign name="arrowleft" size={20} color="#fff" />
              </TouchableOpacity>
              <Animated.View style={{ opacity: fadeAnim, alignItems: 'center', width: '100%' }}>
                <View style={[styles.logoContainer, dynamicStyles.logoContainer]}>
                  <Image
                    style={[styles.Logo, dynamicStyles.logo]}
                    source={require('../assets/images/Logofundo.png')}
                    accessibilityLabel="Logo do aplicativo"
                  />
                </View>
                <View style={[styles.formContainer, dynamicStyles.formPadding]}>
                  <Text style={[styles.titulo, dynamicStyles.titulo]}>Cadastro</Text>
                  {[
                    {
                      placeholder: 'Nome de usuário',
                      value: nome,
                      setter: setNome,
                      error: errors.nome,
                      key: 'nome',
                    },
                    {
                      placeholder: 'Email',
                      value: email,
                      setter: setEmail,
                      error: errors.email,
                      key: 'email',
                      props: { keyboardType: 'email-address', autoCapitalize: 'none' },
                    },
                    {
                      placeholder: 'Senha',
                      value: senha,
                      setter: setSenha,
                      error: errors.senha,
                      key: 'senha',
                      props: { secureTextEntry: true },
                    },
                  ].map(({ placeholder, value, setter, error, key, props = {} }) => (
                    <React.Fragment key={key}>
                      <TextInput
                        style={[
                          styles.input,
                          dynamicStyles.input,
                          error && { borderColor: '#ff8080' },
                        ]}
                        placeholder={placeholder}
                        placeholderTextColor="#FFF"
                        value={value}
                        onChangeText={(text) => {
                          setter(text);
                          if (error) {
                            setErrors((prevErrors) => ({
                              ...prevErrors,
                              [key]: null
                            }));
                          }
                        }}
                        autoCorrect={false}
                        {...props}
                      />
                      {error && <Text style={styles.error}>{error}</Text>}
                    </React.Fragment>
                  ))}
                  <TouchableOpacity
                    activeOpacity={0.85}
                    style={[
                      styles.botao,
                      dynamicStyles.botao,
                      isPressing && { transform: [{ scale: 0.97 }], backgroundColor: '#26144d' },
                      loading && { opacity: 0.7 },
                    ]}
                    disabled={loading}
                    onPressIn={() => setIsPressing(true)}
                    onPressOut={() => setIsPressing(false)}
                    onPress={handleCadastro}
                  >
                    <Text style={[styles.textoBotao, dynamicStyles.textoBotao]}>
                      {loading ? 'Enviando...' : 'Cadastrar'}
                    </Text>
                  </TouchableOpacity>
                </View>
              </Animated.View>
            </ScrollView>
          </KeyboardAvoidingView>
        </SafeAreaView>
      </LinearGradient>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  gradient: { flex: 1 },
  safe: { flex: 1 },
  flex: { flex: 1 },
  logoContainer: { alignSelf: 'center' },
  Logo: { resizeMode: 'contain' },
  formContainer: { width: '90%', maxWidth: 450 },
  titulo: { fontFamily: 'negrito', color: '#fff', textAlign: 'center' },
  input: {
    borderRadius: 25,
    fontSize: 20,
    borderWidth: 2,
    borderColor: "#FFF",
    fontFamily: "normal",
    color: "#FFF",
    shadowColor: "#000",
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 7 },
    shadowRadius: 4,
    elevation: 5,
    margin: 10,
    backgroundColor: "#1D143642",
    minHeight: 70,
    height: 70,
    paddingVertical: 10,
    textAlignVertical: 'center',
  },
  botao: {
    height: 70,
    backgroundColor: '#1d1436',
    borderColor: '#8000D5',
    alignItems: 'center',
    textAlign: 'center',
  },
  textoBotao: { color: '#FFF', fontFamily: 'negrito' },
  error: {
    color: '#ff8080',
    textAlign: 'center',
    marginTop: 4,
    fontFamily: 'normal',
  },
});

export default Cadastro;
