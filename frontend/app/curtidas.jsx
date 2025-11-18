import { AntDesign, FontAwesome } from "@expo/vector-icons";
import { LinearGradient } from 'expo-linear-gradient';
import { useEffect, useRef, useState } from 'react';
import {
  AccessibilityInfo,
  Animated,
  Platform,
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  useWindowDimensions,
  View
} from 'react-native';

const App = ({ navigation = { goBack: () => {} } }) => {
  const scaleAnim = useRef(new Animated.Value(1)).current;
  const [showParticles, setShowParticles] = useState(false);
  const { width, height } = useWindowDimensions();
  const [reduceMotionEnabled, setReduceMotionEnabled] = useState(false);

  useEffect(() => {
    if (Platform.OS === 'ios' || Platform.OS === 'android') {
      AccessibilityInfo.isReduceMotionEnabled().then((result) => {
        setReduceMotionEnabled(result);
      });
    }
  }, []);

  const particles = [
    useRef(new Animated.Value(0)).current,
    useRef(new Animated.Value(0)).current,
    useRef(new Animated.Value(0)).current,
  ];

  const handlePress = () => {
    if (reduceMotionEnabled) return;

    Animated.sequence([
      Animated.timing(scaleAnim, {
        toValue: 1.3,
        duration: 150,
        useNativeDriver: true,
      }),
      Animated.timing(scaleAnim, {
        toValue: 1,
        duration: 150,
        useNativeDriver: true,
      }),
    ]).start();

    setShowParticles(true);
    particles.forEach((particle, index) => {
      particle.setValue(0);
      Animated.timing(particle, {
        toValue: 1,
        duration: 600,
        delay: index * 100,
        useNativeDriver: true,
      }).start(() => {
        if (index === particles.length - 1) {
          setShowParticles(false);
        }
      });
    });
  };

  const isPortrait = height >= width;

  const headerFontSize = Math.min(Math.max(width * 0.06, 18), 28);
  const mainHeartSize = Math.min(Math.max(width * 0.25, 80), 130);
  const particleSize = Math.min(Math.max(width * 0.045, 15), 22);
  const contentTitleSize = Math.min(Math.max(width * 0.055, 17), 24);
  const contentDescSize = Math.min(Math.max(width * 0.038, 13), 18);
  const navFontSize = Math.min(Math.max(width * 0.04, 14), 20);
  const iconButtonPadding = Math.min(Math.max(width * 0.04, 12), 20);
  const iconButtonBorderRadius = Math.min(Math.max(width * 0.3, 50), 90);

  return (
    <LinearGradient
    colors={['#962fbf', '#d62976', '#fa7e1e', '#feda75',]} 
    style={styles.container}
    start={{ x: 0.5, y: 0 }}    
    end={{ x: 0.5, y: 1 }}     
  >
  

      <SafeAreaView style={{ flex: 1 }}>
        <View style={[styles.header, { paddingVertical: height * 0.035 }]}>
          <Text
            accessible
            accessibilityRole="header"
            accessibilityLabel="Título Suas Curtidas"
            style={[styles.headerText, { fontSize: headerFontSize }]}
          >
            Suas Curtidas
          </Text>
        </View>
         <TouchableOpacity style={styles.backCircle} onPress={() => navigation.goBack()}>
          <AntDesign name="arrowleft" size={20} color="#fff" />
        </TouchableOpacity>

        <View
          style={[
            styles.iconContainer,
            { marginTop: height * 0.03, flexDirection: isPortrait ? 'column' : 'row' },
          ]}
        >
          <Pressable
            onPress={handlePress}
            accessibilityRole="button"
            accessibilityLabel="Botão de Curtir"
            accessibilityHint="Ativa animação de coração"
            disabled={reduceMotionEnabled}
          >
            <Animated.View
              style={[
                styles.iconButton,
                {
                  transform: [{ scale: scaleAnim }],
                  padding: iconButtonPadding,
                  borderRadius: iconButtonBorderRadius,
                  shadowOffset: { width: 0, height: 6 },
                  shadowOpacity: 0.35,
                  shadowRadius: 7,
                  elevation: 10,
                },
              ]}
            >
              <FontAwesome name="heart" size={mainHeartSize} color="#fff" style={styles.backHeart} />
              <FontAwesome name="heart" size={mainHeartSize * 0.9} color="#ffd900" />
            </Animated.View>
          </Pressable>

          {!reduceMotionEnabled && showParticles &&
            particles.map((anim, i) => {
              const translateY = anim.interpolate({
                inputRange: [0, 1],
                outputRange: [0, -90 - i * 15],
              });

              const translateX = anim.interpolate({
                inputRange: [0, 1],
                outputRange: [0, (i % 2 === 0 ? -1 : 1) * (25 + i * 12)],
              });

              const opacity = anim.interpolate({
                inputRange: [0, 1],
                outputRange: [1, 0],
              });

              const colors = ['#cc00ff', '#ff9900', '#ffe600'];

              return (
                <Animated.View
                  key={i}
                  style={{
                    position: 'absolute',
                    top: height * 0.4,
                    transform: [{ translateY }, { translateX }],
                    opacity,
                  }}
                >
                  <FontAwesome name="heart" size={particleSize} color={colors[i % colors.length]} />
                </Animated.View>
              );
            })}
        </View>

        <View style={[styles.content, { paddingHorizontal: width * 0.1 }]}>
          <Text
            accessible
            accessibilityRole="text"
            accessibilityLabel="Mensagem principal ainda sem curtidas"
            style={[styles.contentText1, { fontSize: contentTitleSize }]}
          >
            Ainda sem curtidas
          </Text>
          <Text
            accessible
            accessibilityRole="text"
            accessibilityLabel="Descrição para começar a descobrir músicas"
            style={[styles.contentText2, { fontSize: contentDescSize, marginTop: 12 }]}
          >
            Comece a descobrir músicas para ver suas curtidas aqui!
          </Text>
        </View>

        <View style={[styles.nav, { paddingVertical: height * 0.025 }]}>
          {['Player', 'Curtidas', 'Perfil'].map((item, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.navItem, { paddingHorizontal: width * 0.06 }]}
              activeOpacity={0.7}
              accessibilityRole="button"
              accessibilityLabel={`Navegar para ${item}`}
            >
              <Text style={[styles.navText1, { fontSize: navFontSize }]}>{item}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </SafeAreaView>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 20,
    alignItems: 'center',
  },
  headerText: {
    color: '#fff',
    fontWeight: 'bold',
  },
  iconContainer: {
    flex: 1.5,
    justifyContent: 'center',
    alignItems: 'center',
    position: 'relative',
  },
  backCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: "rgba(255,255,255,0.18)",
    alignItems: "center",
    justifyContent: "center",
    marginTop: 12,
    marginLeft: -2,
  },
  
  iconButton: {
    borderRadius: 50,
    padding: 10,
    elevation: 5,
  },
  nav: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#000000',
    paddingVertical: 10,
    marginBottom: '0%',
    marginLeft: '0%',
    marginRight: '0%',
  },
  navItem: {
    padding: 10,
  },
  backHeart: {
    position: 'absolute',
    top: 5,
    left: 5,
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  contentText1: {
    color: '#ffffff',
    textAlign: 'center',
  },
  contentText2: {
    color: '#ffffff',
    textAlign: 'center',
  },
  navText1: {
    color: '#ff3cf5',
  },
});

export default App;
