import React, { useState, useEffect } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  Alert,
} from 'react-native';

// Dummy data
const dummyData = [
  { id: 1, name: 'Beer A', brewery: 'Brewery A', style: 'Style A', abv: 5.0, ibu: 20 },
  { id: 2, name: 'Beer B', brewery: 'Brewery B', style: 'Style B', abv: 6.0, ibu: 25 },
];

export default function App() {
  const [name, setName] = useState('');
  const [brewery, setBrewery] = useState('');
  const [style, setStyle] = useState('');
  const [abv, setAbv] = useState('');
  const [ibu, setIbu] = useState('');
  const [beers, setBeers] = useState(dummyData);

  const handleAddBeer = () => {
    if (!name || !brewery || !style || !abv || !ibu) {
      Alert.alert('Error', 'Please fill in all fields.');
      return;
    }

    const newBeer = {
      id: Math.random().toString(),
      name,
      brewery,
      style,
      abv: parseFloat(abv),
      ibu: parseFloat(ibu),
    };

    setBeers(prevBeers => [...prevBeers, newBeer]);
    setName('');
    setBrewery('');
    setStyle('');
    setAbv('');
    setIbu('');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Beer Tracker</Text>

      <View style={styles.form}>
        <TextInput
          style={styles.input}
          placeholder="Name"
          value={name}
          onChangeText={text => setName(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="Brewery"
          value={brewery}
          onChangeText={text => setBrewery(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="Style"
          value={style}
          onChangeText={text => setStyle(text)}
        />
        <TextInput
          style={styles.input}
          placeholder="ABV"
          value={abv}
          onChangeText={text => setAbv(text)}
          keyboardType="numeric"
        />
        <TextInput
          style={styles.input}
          placeholder="IBU"
          value={ibu}
          onChangeText={text => setIbu(text)}
          keyboardType="numeric"
        />
        <TouchableOpacity style={styles.addButton} onPress={handleAddBeer}>
          <Text style={styles.addButtonText}>Add Beer</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.subtitle}>Beer List</Text>
      <FlatList
        data={beers}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <View style={styles.beerItem}>
            <Text>{item.name} ({item.style}) - ABV: {item.abv}%, IBU: {item.ibu}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
  },
  form: {
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
  addButton: {
    backgroundColor: 'blue',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  addButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  beerItem: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 5,
    padding: 10,
    marginBottom: 10,
  },
});

