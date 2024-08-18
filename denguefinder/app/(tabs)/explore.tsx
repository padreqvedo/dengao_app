import React, { useState, useEffect } from "react";
import MapView, { Marker } from "react-native-maps";
import { StyleSheet, View, Text } from "react-native";

// Suponha que você tenha o JSON salvo em um arquivo chamado `data.json`
import data from '@/assets/casos_por_bairro_ajustados.json'; // Ajuste o caminho conforme necessário

export default function Explore() {
  const [markers, setMarkers] = useState<{ id: number; coordinate: { latitude: number; longitude: number; }; title: string; number: number; }[]>([]);

  useEffect(() => {
    // Mapeia os dados JSON para o formato necessário
    const newMarkers = data.map((item, index) => ({
      id: index + 1,
      coordinate: { latitude: item.latitude, longitude: item.longitude },
      title: item.Bairro,
      number: item.Casos_Positivos,
    }));
    setMarkers(newMarkers);
  }, []);

  const renderMarkers = () => {
    return markers.map((marker) => (
      <Marker key={marker.id} coordinate={marker.coordinate} title={marker.title}>
        <CustomMarker number={marker.number} />
      </Marker>
    ));
  };

  return (
    <View style={styles.container}>
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: -22.1892, // Ajuste conforme a localização central desejada
          longitude: -47.398,
          latitudeDelta: 0.0922,
          longitudeDelta: 0.0421,
        }}
      >
        {renderMarkers()}
      </MapView>
    </View>
  );
}

const CustomMarker = ({ number }: { number: number }) => {
  const size = 10 + number * 1.5; // Ajusta o tamanho da bola com base no número

  return (
    <View style={[styles.marker, { width: size, height: size, borderRadius: size / 2 }]}>
      <Text style={styles.markerText}>{number}</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  map: {
    width: "100%",
    height: "100%",
  },
  marker: {
    backgroundColor: "rgba(255, 0, 0, 0.3)", // Cor vermelha com mais transparência
    justifyContent: "center",
    alignItems: "center",
  },
  markerText: {
    color: "white",
    fontWeight: "bold",
    fontSize: 10, // Ajusta o tamanho do texto
  },
});
